#!/bin/bash
set -e

echo "🚀 开始安装 TheNEWs..."

# 克隆项目
if [ ! -d ~/TheNEWs ]; then
    echo "📥 克隆项目..."
    git clone https://github.com/fezeryang/TheNEWs.git ~/TheNEWs
else
    echo "📁 项目已存在，跳过克隆"
fi

cd ~/TheNEWs

# 创建虚拟环境
if [ ! -d venv ]; then
    echo "🐍 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
echo "📦 安装依赖..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q litellm feedparser requests pyyaml python-dateutil

echo ""
echo "✅ 安装完成！"
echo ""
echo "📝 下一步："
echo "   1. 设置 API Key: export AI_API_KEY='your-key'"
echo "   2. 运行: cd ~/TheNEWs && ./run.sh"
