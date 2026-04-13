@echo off
echo 正在安装 Python 依赖...
pip install fastapi "uvicorn[standard]" httpx openpyxl Pillow python-multipart pydantic aiofiles

echo.
echo 正在安装 PaddleOCR (可能需要几分钟)...
pip install paddleocr

echo.
echo 安装完成！运行 start.bat 启动应用。
pause
