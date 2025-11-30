@echo off
echo 🚀 Starting Document Generator System...
echo.

echo 📋 This will start both backend and frontend services
echo Backend will run on http://localhost:5000
echo Frontend will run on http://localhost:5173
echo.

REM 启动后端
echo 🛠️ Starting Backend...
start "Flask Backend" cmd /k "cd /d %~dp0 && start-backend.bat"

REM 等待几秒让后端启动
timeout /t 3 /nobreak >nul

REM 启动前端
echo 🎨 Starting Frontend...
start "React Frontend" cmd /k "cd /d %~dp0 && start-frontend.bat"

echo ✅ Both services are starting!
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window (services will continue running)
pause >nul