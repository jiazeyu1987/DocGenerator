#!/bin/bash

echo "🚀 Starting React Frontend..."
echo

cd "$(dirname "$0")/frontend"

# 检查是否已安装依赖
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# 启动开发服务器
echo "🌟 Starting React dev server on http://localhost:5173"
echo
npm run dev