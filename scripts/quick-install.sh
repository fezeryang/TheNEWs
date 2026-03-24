#!/bin/bash
# TheNEWs 快速安装并运行脚本
# 使用方法: bash <(curl -s https://raw.githubusercontent.com/fezeryang/TheNEWs/master/scripts/quick-install.sh)

set -e

echo "🚀 TheNEWs 快速安装"
echo "===================="
echo ""

# 检查依赖
command -v python3 >/dev/null 2>&1 || { echo "❌ 需要 Python 3"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ 需要 Git"; exit 1; }

# 克隆项目
INSTALL_DIR="$HOME/TheNEWs"
if [ ! -d "$INSTALL_DIR" ]; then
    echo "📥 克隆项目到 $INSTALL_DIR..."
    git clone https://github.com/fezeryang/TheNEWs.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 创建虚拟环境
if [ ! -d venv ]; then
    echo "🐍 创建虚拟环境..."
    python3 -m venv venv
fi

# 安装依赖
echo "📦 安装依赖..."
source venv/bin/activate
pip install -q litellm feedparser requests pyyaml python-dateutil

echo ""
echo "✅ 安装完成！"
echo ""
echo "⚠️  请先设置 API Key："
echo "   export AI_API_KEY='sk-xxxxxxxxxxxxx'"
echo ""
echo "📍 DeepSeek 获取: https://platform.deepseek.com/api_keys"
echo ""
echo "运行前请检查 API Key 是否设置："
if [ -z "$AI_API_KEY" ]; then
    echo "❌ AI_API_KEY 未设置"
    echo ""
    read -p "是否现在设置 API Key? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入你的 API Key: " api_key
        export AI_API_KEY="$api_key"
        echo "已设置 API Key（仅当前会话有效）"
        echo ""
        echo "💡 永久设置: echo 'export AI_API_KEY=\"$api_key\"' >> ~/.bashrc"
    fi
else
    echo "✅ AI_API_KEY 已设置"
    echo ""
    read -p "是否现在运行 TheNEWs? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 正在运行..."
        python -m trendradar
    fi
fi
