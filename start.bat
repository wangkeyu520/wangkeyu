@echo off
chcp 65001 >nul

echo ============================================
echo   Sunny Tea House AI评价生成器 - 启动脚本
echo   (Element Plus 版本)
echo ============================================

echo.
echo [1/4] 创建后端虚拟环境...
if not exist "backend\.venv" (
    python -m venv backend\.venv
    echo 虚拟环境创建成功
) else (
    echo 虚拟环境已存在
)

echo.
echo [2/4] 安装后端依赖...
call backend\.venv\Scripts\activate.bat
pip install -r backend\requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
echo 后端依赖安装完成

echo.
echo [3/4] 安装前端依赖...
cd frontend
npm install --registry=https://registry.npmmirror.com
echo 前端依赖安装完成

echo.
echo [4/4] 启动服务...
echo.
echo 后端服务: http://localhost:8000
echo 前端页面: http://localhost:5173
echo.

start "" cmd /k "cd ..\backend && .venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"
start "" cmd /k "cd ..\frontend && npm run dev"

echo 服务启动中，请等待几秒后打开浏览器访问 http://localhost:5173
pause