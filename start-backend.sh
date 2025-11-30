#!/bin/bash

echo "🚀 Starting Flask Backend..."
echo

cd "$(dirname "$0")/backend"

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# 安装依赖
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# 创建模板目录
if [ ! -d "templates_store" ]; then
    mkdir templates_store
    echo "📁 Created templates_store directory"
fi

# 启动服务
echo "🌟 Starting Flask server on http://localhost:5000"
echo
python app.py