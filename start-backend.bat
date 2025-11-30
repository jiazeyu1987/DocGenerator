@echo off
echo 🚀 Starting Flask Backend...
echo.

cd /d "%~dp0backend"

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM 安装依赖
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM 创建模板目录
if not exist "templates_store" (
    mkdir templates_store
    echo 📁 Created templates_store directory
)

REM 启动服务
echo 🌟 Starting Flask server on http://localhost:5000
echo.
python app.py

pause