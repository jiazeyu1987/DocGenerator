#!/usr/bin/env python3
"""
Mermaid流程图处理模块
用于检测、转换和替换Markdown中的Mermaid图表
"""

import re
import tempfile
import subprocess
import os
import uuid
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class MermaidProcessor:
    """Mermaid图表处理器"""

    def __init__(self, output_dir: str = None):
        """
        初始化处理器

        Args:
            output_dir: 图片输出目录，如果为None则使用项目images目录
        """
        # 如果没有指定输出目录，使用项目的images目录
        if output_dir is None:
            # 获取项目根目录（从backend目录向上两级）
            current_dir = Path(__file__).parent
            project_root = current_dir.parent
            self.output_dir = str(project_root / "images")
        else:
            self.output_dir = output_dir

        self.mermaid_blocks: List[Dict] = []
        self.temp_dir: Optional[str] = None

        # 测试模式配置
        self.test_mode = os.environ.get("MERMAID_TEST_MODE", "false").lower() == "true"
        self.test_output_dir = os.environ.get("MERMAID_TEST_OUTPUT_DIR", "d:/tmp/mermaid_test")

        if self.test_mode:
            logger.info(f"MermaidProcessor initialized in test mode")
            logger.info(f"Test output directory: {self.test_output_dir}")

        # Mermaid语法检测模式
        self.mermaid_pattern = re.compile(
            r'```mermaid\s*\n(.*?)\n```',
            re.IGNORECASE | re.DOTALL
        )

        # 支持的Mermaid图表类型
        self.supported_types = [
            'graph', 'flowchart', 'sequenceDiagram', 'classDiagram',
            'stateDiagram', 'stateDiagram-v2', 'erDiagram',
            'journey', 'gantt', 'pie', 'timeline', 'gitgraph'
        ]

    def extract_mermaid_blocks(self, content: str) -> Tuple[str, List[Dict]]:
        """
        提取Markdown中的Mermaid代码块

        Args:
            content: Markdown内容

        Returns:
            Tuple[处理后的内容, Mermaid块列表]
        """
        self.mermaid_blocks = []
        processed_content = content

        # 查找所有Mermaid代码块
        matches = self.mermaid_pattern.findall(content)

        for i, mermaid_code in enumerate(matches):
            mermaid_code = mermaid_code.strip()

            # 验证是否为有效的Mermaid语法
            if not self._is_valid_mermaid(mermaid_code):
                logger.warning(f"Invalid Mermaid syntax detected, skipping: {mermaid_code[:50]}...")
                continue

            # 生成唯一ID和文件名
            block_id = f"diagram-{i + 1}-{uuid.uuid4().hex[:8]}"
            image_filename = f"{block_id}.png"

            # 创建图片引用 - 使用相对路径，Pandoc会正确处理
            image_reference = f"![Mermaid图表](images/{image_filename})"

            # 记录Mermaid块信息
            mermaid_block = {
                'id': block_id,
                'filename': image_filename,
                'code': mermaid_code,
                'original_block': f'```mermaid\n{mermaid_code}\n```',
                'image_reference': image_reference,
                'index': i
            }

            self.mermaid_blocks.append(mermaid_block)

            # 在内容中替换为图片引用
            processed_content = processed_content.replace(
                mermaid_block['original_block'],
                image_reference,
                1  # 只替换第一个匹配项
            )

            logger.info(f"Extracted Mermaid block {block_id}: {mermaid_code[:50]}...")

        logger.info(f"Found {len(self.mermaid_blocks)} Mermaid diagram(s)")
        return processed_content, self.mermaid_blocks

    def _is_valid_mermaid(self, code: str) -> bool:
        """
        验证是否为有效的Mermaid语法

        Args:
            code: Mermaid代码

        Returns:
            是否有效
        """
        code_lower = code.lower().strip()

        # 检查是否以支持的图表类型开头
        for chart_type in self.supported_types:
            if code_lower.startswith(chart_type.lower()):
                return True

        return False

    def setup_output_directory(self, base_dir: str) -> str:
        """
        设置图片输出目录

        Args:
            base_dir: 基础目录（现在不再使用，保持兼容性）

        Returns:
            图片输出目录路径
        """
        # 始终使用配置的输出目录（现在默认是项目images目录）
        images_dir = Path(self.output_dir)

        # 确保目录存在
        images_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Mermaid images will be saved to: {images_dir}")
        return str(images_dir)

    def convert_mermaid_to_image(self, mermaid_code: str, output_path: str,
                                theme: str = 'neutral', background: str = 'white',
                                width: int = 800, height: int = 600) -> bool:
        """
        使用Mermaid CLI将代码转换为图片

        Args:
            mermaid_code: Mermaid代码
            output_path: 输出图片路径
            theme: 主题 (neutral, dark, forest, default)
            background: 背景色
            width: 图片宽度
            height: 图片高度

        Returns:
            转换是否成功
        """
        try:
            # 创建临时Mermaid文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd',
                                           delete=False, encoding='utf-8') as temp_file:
                temp_file.write(mermaid_code)
                temp_mmd_path = temp_file.name

            # 在测试模式下保存原始mermaid代码
            if self.test_mode:
                import json
                from datetime import datetime

                debug_dir = os.path.join(self.test_output_dir, f"mermaid_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                os.makedirs(debug_dir, exist_ok=True)

                # 保存原始代码
                mmd_debug_path = os.path.join(debug_dir, os.path.basename(output_path).replace('.png', '.mmd'))
                with open(mmd_debug_path, 'w', encoding='utf-8') as f:
                    f.write(mermaid_code)
                logger.info(f"Test mode: mermaid code saved to {mmd_debug_path}")

            try:
                # 构建mmdc命令 - 使用完整路径解决Python子进程PATH问题
                mermaid_cli = os.environ.get("MERMAID_CLI", "mmdc")
                # 在Windows下检查是否需要使用完整路径
                if os.name == 'nt' and mermaid_cli == 'mmdc':
                    # 尝试常见的npm安装路径
                    possible_paths = [
                        r"C:\Users\BJB110\AppData\Roaming\npm\mmdc.cmd",
                        r"C:\Users\{}\AppData\Roaming\npm\mmdc.cmd".format(os.getenv('USERNAME', 'BJB110')),
                        "mmdc.cmd"  # 备用
                    ]
                    for path in possible_paths:
                        if os.path.exists(path) or path == "mmdc.cmd":
                            mermaid_cli = path
                            break

                cmd = [
                    mermaid_cli,
                    '-i', temp_mmd_path,
                    '-o', output_path,
                    '-t', theme,
                    '-b', background,
                    '-w', str(width),
                    '-H', str(height)
                ]

                logger.info(f"Running Mermaid CLI: {' '.join(cmd)}")

                # 执行转换
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30秒超时
                )

                if result.returncode == 0:
                    # 验证输出文件是否存在
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        file_size = os.path.getsize(output_path)
                        logger.info(f"✓ Successfully generated image: {output_path} ({file_size} bytes)")

                        # 在测试模式下复制图片到调试目录
                        if self.test_mode:
                            debug_image_path = os.path.join(debug_dir, os.path.basename(output_path))
                            import shutil
                            shutil.copy2(output_path, debug_image_path)
                            logger.info(f"Test mode: image copied to {debug_image_path}")

                        return True
                    else:
                        logger.error(f"Mermaid CLI completed but output file is empty: {output_path}")
                        return False
                else:
                    logger.error(f"✗ Mermaid CLI failed with code {result.returncode}")
                    logger.error(f"stderr: {result.stderr}")
                    logger.error(f"stdout: {result.stdout}")

                    # 在测试模式下保存错误信息
                    if self.test_mode:
                        error_info = {
                            "return_code": result.returncode,
                            "stderr": result.stderr,
                            "stdout": result.stdout,
                            "command": ' '.join(cmd),
                            "output_path": output_path
                        }
                        error_file = os.path.join(debug_dir, "conversion_error.json")
                        with open(error_file, 'w', encoding='utf-8') as f:
                            json.dump(error_info, f, indent=2)
                        logger.info(f"Test mode: error info saved to {error_file}")

                    return False

            except subprocess.TimeoutExpired:
                logger.error(f"✗ Mermaid conversion timeout for: {output_path}")
                return False

            finally:
                # 清理临时文件（非测试模式）
                if not self.test_mode:
                    try:
                        os.unlink(temp_mmd_path)
                    except OSError:
                        pass
                else:
                    logger.info(f"Test mode: temporary file preserved at {temp_mmd_path}")

        except Exception as e:
            logger.error(f"✗ Error converting Mermaid to image: {e}")
            return False

    def process_all_mermaid_blocks(self, base_dir: str) -> Tuple[List[str], List[str]]:
        """
        处理所有提取的Mermaid块

        Args:
            base_dir: 基础目录

        Returns:
            Tuple[成功生成的图片路径列表, 失败的块索引列表]
        """
        if not self.mermaid_blocks:
            return [], []

        # 设置输出目录
        images_dir = self.setup_output_directory(base_dir)

        successful_images = []
        failed_blocks = []

        for i, block in enumerate(self.mermaid_blocks):
            output_path = os.path.join(images_dir, block['filename'])

            logger.info(f"Processing Mermaid block {i + 1}/{len(self.mermaid_blocks)}: {block['id']}")

            # 转换Mermaid代码为图片
            if self.convert_mermaid_to_image(block['code'], output_path):
                successful_images.append(output_path)
                logger.info(f"✓ Successfully converted {block['id']}")
            else:
                failed_blocks.append(block['index'])
                logger.error(f"✗ Failed to convert {block['id']}")

        logger.info(f"Mermaid processing completed: {len(successful_images)} successful, {len(failed_blocks)} failed")
        return successful_images, failed_blocks

    def restore_failed_blocks(self, content: str, failed_indices: List[int]) -> str:
        """
        恢复转换失败的Mermaid代码块

        Args:
            content: 已处理的内容
            failed_indices: 失败的块索引列表

        Returns:
            恢复后的内容
        """
        restored_content = content

        for index in sorted(failed_indices, reverse=True):
            # 从末尾开始恢复，避免位置偏移
            if index < len(self.mermaid_blocks):
                block = self.mermaid_blocks[index]
                restored_content = restored_content.replace(
                    block['image_reference'],
                    block['original_block'],
                    1
                )
                logger.info(f"Restored original Mermaid block: {block['id']}")

        return restored_content

    def cleanup(self):
        """清理临时文件"""
        # 由于我们现在使用项目目录而不是临时目录，不需要清理图片文件
        # 只清理测试模式下可能创建的临时目录
        if self.temp_dir and os.path.exists(self.temp_dir):
            if self.test_mode:
                logger.info(f"Test mode: temporary directory preserved at {self.temp_dir}")
            else:
                try:
                    shutil.rmtree(self.temp_dir, ignore_errors=True)
                    logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temporary directory: {e}")

        # 不再清理项目images目录中的图片文件，因为它们需要被保留用于文档中

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


def process_markdown_with_mermaid(content: str, base_dir: str) -> Tuple[str, List[str]]:
    """
    便捷函数：处理Markdown内容中的Mermaid图表

    Args:
        content: Markdown内容
        base_dir: 基础目录

    Returns:
        Tuple[处理后的内容, 生成的图片路径列表]
    """
    with MermaidProcessor() as processor:
        # 提取Mermaid块
        processed_content, mermaid_blocks = processor.extract_mermaid_blocks(content)

        if not mermaid_blocks:
            # 没有找到Mermaid块，直接返回原内容
            return content, []

        # 处理所有Mermaid块
        successful_images, failed_blocks = processor.process_all_mermaid_blocks(base_dir)

        # 恢复失败的块
        if failed_blocks:
            processed_content = processor.restore_failed_blocks(processed_content, failed_blocks)

        return processed_content, successful_images