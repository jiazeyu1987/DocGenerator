import os
import tempfile
import subprocess
import logging
import re
import shutil
import atexit
from pathlib import Path
from threading import Timer

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全局字典存储需要清理的临时文件
_temp_files_to_cleanup = {}

def delayed_cleanup(file_path, delay=300):
    """延迟清理临时文件"""
    def cleanup():
        try:
            if file_path.exists():
                shutil.rmtree(file_path, ignore_errors=True)
                logger.info(f"Cleaned up temporary directory: {file_path}")
            # 从全局字典中移除
            _temp_files_to_cleanup.pop(str(file_path), None)
        except Exception as e:
            logger.warning(f"Failed to cleanup temporary directory: {e}")

    # 添加到全局字典
    _temp_files_to_cleanup[str(file_path)] = cleanup

    # 设置延迟清理
    timer = Timer(delay, cleanup)
    timer.daemon = True  # 设置为守护线程，主程序退出时不会阻止
    timer.start()

# 注册退出时的清理函数
def cleanup_all_temp_files():
    """清理所有临时文件"""
    for cleanup_func in _temp_files_to_cleanup.values():
        try:
            cleanup_func()
        except:
            pass

atexit.register(cleanup_all_temp_files)


def is_safe_filename(filename: str) -> bool:
    """验证文件名是否安全，防止路径遍历攻击"""
    if not filename:
        return False

    # 检查路径遍历攻击
    if '..' in filename or '/' in filename or '\\' in filename:
        return False

    # 检查文件名不以点开头（隐藏文件）
    if filename.startswith('.'):
        return False

    # 检查非法字符
    illegal_chars = '<>:"|?*\0'
    if any(char in filename for char in illegal_chars):
        return False

    # 检查文件名长度
    if len(filename) > 255:
        return False

    return True

def validate_template_name(template_name: str, template_folder: str) -> bool:
    """验证模板文件名是否安全"""
    if not template_name or not template_name.endswith('.docx'):
        return False
    if not is_safe_filename(template_name):
        return False

    # 确保文件路径在模板目录内
    template_path = Path(template_folder) / template_name
    try:
        template_path.resolve().relative_to(Path(template_folder).resolve())
        return True
    except ValueError:
        return False

def check_pandoc_available() -> bool:
    """检查Pandoc是否可用"""
    try:
        subprocess.run(['pandoc', '--version'],
                      capture_output=True, check=True, timeout=10)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.config["UPLOAD_FOLDER"] = os.environ.get(
        "UPLOAD_FOLDER", str(Path(tempfile.gettempdir()) / "docgen_uploads")
    )
    app.config["TEMPLATE_FOLDER"] = os.environ.get(
        "TEMPLATE_FOLDER", str(Path(app.root_path) / "templates_store")
    )
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["TEMPLATE_FOLDER"], exist_ok=True)

    # 启动时检查Pandoc
    if not check_pandoc_available():
        logger.warning("Pandoc not found. Please install pandoc to use conversion features.")
    else:
        logger.info("Pandoc is available")

    @app.route("/api/health", methods=["GET"])
    def health() -> tuple[dict, int]:
        return {
            "status": "ok",
            "pandoc_available": check_pandoc_available()
        }, 200

    @app.route("/api/templates", methods=["GET"])
    def list_templates():
        templates_dir = Path(app.config["TEMPLATE_FOLDER"])
        templates = [
            {
                "name": p.name,
                "path": str(p.resolve()),
            }
            for p in templates_dir.glob("*.docx")
        ]
        return jsonify(templates)

    @app.route("/api/convert", methods=["POST"])
    def convert_markdown():
        if not check_pandoc_available():
            return {"error": "Pandoc not available. Please install pandoc first."}, 503

        if "file" not in request.files:
            logger.warning("Conversion request without file")
            return {"error": "No file part in request"}, 400

        file = request.files["file"]
        if file.filename == "":
            logger.warning("Conversion request with empty filename")
            return {"error": "No file selected"}, 400

        # 验证文件类型
        if not file.filename.lower().endswith(('.md', '.markdown')):
            logger.warning(f"Invalid file type uploaded: {file.filename}")
            return {"error": "Only Markdown files (.md, .markdown) are allowed"}, 400

        # 验证文件名安全性
        if not is_safe_filename(file.filename):
            logger.warning(f"Unsafe filename detected: {file.filename}")
            return {"error": "Invalid filename"}, 400

        template_name = request.form.get("template")

        # 验证模板名称
        if template_name:
            if not validate_template_name(template_name, app.config["TEMPLATE_FOLDER"]):
                logger.warning(f"Invalid template requested: {template_name}")
                return {"error": "Invalid template name"}, 400

        logger.info(f"Starting conversion for file: {file.filename}")

        upload_dir = Path(app.config["UPLOAD_FOLDER"])
        upload_dir.mkdir(parents=True, exist_ok=True)

        # 验证文件内容（简单检查是否为文本文件）
        try:
            file_content = file.read(1024)  # 读取前1KB检查
            file.seek(0)  # 重置文件指针

            # 检查是否为文本文件
            if b'\x00' in file_content[:512]:  # 检查空字节，通常表示二进制文件
                logger.warning(f"Binary file detected: {file.filename}")
                return {"error": "File appears to be binary, not text"}, 400

        except Exception as e:
            logger.error(f"Error reading file content: {e}")
            return {"error": "Error reading uploaded file"}, 400

        # 使用不自动删除的临时目录
        tmpdir_path = Path(tempfile.mkdtemp(dir=upload_dir))
        input_path = tmpdir_path / "input.md"
        output_path = tmpdir_path / "output.docx"

        try:
            file.save(input_path)

            cmd = ["pandoc", str(input_path), "-o", str(output_path)]

            if template_name:
                tpl_path = Path(app.config["TEMPLATE_FOLDER"]) / template_name
                if tpl_path.is_file():
                    cmd.extend(["--reference-doc", str(tpl_path)])
                    logger.info(f"Using template: {template_name}")
                else:
                    logger.warning(f"Template file not found: {template_name}")

            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=60  # 60秒超时
                )
                logger.info(f"Pandoc conversion successful for {file.filename}")
            except subprocess.TimeoutExpired:
                logger.error(f"Pandoc conversion timeout for {file.filename}")
                return {"error": "Conversion timeout - file may be too large or complex"}, 500
            except FileNotFoundError:
                logger.error("Pandoc not found during conversion")
                return {
                    "error": "Pandoc not found. Please install pandoc and ensure it is in PATH."
                }, 500
            except subprocess.CalledProcessError as exc:
                logger.error(f"Pandoc conversion failed for {file.filename}: {exc.stderr}")
                return {
                    "error": "Pandoc conversion failed",
                    "details": exc.stderr,
                }, 500

            if not output_path.exists():
                logger.error(f"Output file was not created for {file.filename}")
                return {"error": "Output file was not created"}, 500

            # 复制文件到另一个临时位置，避免文件锁定
            final_output_path = tmpdir_path / "final_output.docx"
            shutil.copy2(output_path, final_output_path)

            # 清理原始的pandoc输出文件
            if output_path.exists():
                output_path.unlink()

            # 设置延迟清理，给文件下载留出足够时间
            delayed_cleanup(tmpdir_path, delay=300)  # 5分钟后清理

            return send_file(
                final_output_path,
                as_attachment=True,
                download_name="document.docx",
                mimetype=(
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ),
            )

        except Exception as e:
            # 如果出错，立即清理临时目录
            try:
                if tmpdir_path.exists():
                    shutil.rmtree(tmpdir_path, ignore_errors=True)
                    logger.info(f"Cleaned up temporary directory due to error: {tmpdir_path}")
            except:
                pass
            logger.error(f"Unexpected error during conversion: {e}")
            return {"error": "Internal server error"}, 500

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)

