@echo off
echo 🚀 Starting React Frontend...
echo.

cd /d "%~dp0frontend"

REM 检查是否已安装依赖
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
)

REM 启动开发服务器
echo 🌟 Starting React dev server on http://localhost:5173
echo.
npm run dev

pause