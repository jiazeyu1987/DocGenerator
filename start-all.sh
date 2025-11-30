#!/bin/bash

echo "🚀 Starting Document Generator System..."
echo

echo "📋 This will start both backend and frontend services"
echo "Backend will run on http://localhost:5000"
echo "Frontend will run on http://localhost:5173"
echo

# 启动后端
echo "🛠️ Starting Backend..."
gnome-terminal --tab --title="Backend" -- bash -c "cd $(pwd) && ./start-backend.sh; exec bash"

# 等待几秒让后端启动
sleep 3

# 启动前端
echo "🎨 Starting Frontend..."
gnome-terminal --tab --title="Frontend" -- bash -c "cd $(pwd) && ./start-frontend.sh; exec bash"

echo "✅ Both services are starting!"
echo
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo
echo "Press Ctrl+C to exit this window (services will continue running)"

# 保持脚本运行
wait