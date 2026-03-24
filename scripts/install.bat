@echo off
echo 🚀 开始安装 TheNEWs...

if not exist "%USERPROFILE%\TheNEWs" (
    echo 📥 克隆项目...
    git clone https://github.com/fezeryang/TheNEWs.git "%USERPROFILE%\TheNEWs"
) else (
    echo 📁 项目已存在，跳过克隆
)

cd /d "%USERPROFILE%\TheNEWs"

if not exist venv (
    echo 🐍 创建虚拟环境...
    python -m venv venv
)

echo 📦 安装依赖...
call venv\Scripts\activate.bat
pip install -q --upgrade pip
pip install -q litellm feedparser requests pyyaml python-dateutil

echo.
echo ✅ 安装完成！
echo.
echo 📝 下一步：
echo    1. 设置 API Key: set AI_API_KEY=your-key
echo    2. 运行: run.bat
