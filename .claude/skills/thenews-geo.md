---
name: thenews-geo
description: 热点新闻GEO借势分析 - 含内嵌脚本 | Hot news AI analysis with embedded install/run scripts
version: 2.0.0
author: fezeryang
repository: https://github.com/fezeryang/TheNEWs
---

# TheNEWs - 热点新闻 GEO 借势分析

> 加载此 skill 后，Claude 可直接执行以下操作：
> - 自动安装项目
> - 配置 API Key
> - 运行热点分析
> - 查看生成结果

---

## 脚本仓库

以下脚本已嵌入此 skill，Claude 可直接读取使用：

### 1. Linux/Mac 一键安装脚本

```bash
#!/bin/bash
# 文件名: install.sh
set -e

echo "🚀 开始安装 TheNEWs..."

# 检查依赖
command -v python3 >/dev/null 2>&1 || { echo "❌ 需要 Python 3"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ 需要 Git"; exit 1; }

# 克隆项目
if [ ! -d ~/TheNEWs ]; then
    echo "📥 克隆项目..."
    git clone https://github.com/fezeryang/TheNEWs.git ~/TheNEWs
else
    echo "📁 项目已存在"
fi

cd ~/TheNEWs

# 创建虚拟环境
if [ ! -d venv ]; then
    echo "🐍 创建虚拟环境..."
    python3 -m venv venv
fi

# 安装依赖
echo "📦 安装依赖..."
source venv/bin/activate
pip install -q litellm feedparser requests pyyaml python-dateutil

echo "✅ 安装完成！"
echo "📝 请设置 API Key: export AI_API_KEY='your-key'"
```

### 2. Linux/Mac 运行脚本

```bash
#!/bin/bash
# 文件名: run.sh
cd ~/TheNEWs
[ -d venv ] && source venv/bin/activate
python -m trendradar "$@"
```

### 3. Windows 安装脚本

```bat
@echo off
REM 文件名: install.bat

echo 🚀 开始安装 TheNEWs...

where git >nul 2>nul || echo ❌ 需要 Git && exit /b 1
where python >nul 2>nul || echo ❌ 需要 Python && exit /b 1

if not exist "%USERPROFILE%\TheNEWs" (
    echo 📥 克隆项目...
    git clone https://github.com/fezeryang/TheNEWs.git "%USERPROFILE%\TheNEWs"
)

cd /d "%USERPROFILE%\TheNEWs"

if not exist venv (
    echo 🐍 创建虚拟环境...
    python -m venv venv
)

echo 📦 安装依赖...
call venv\Scripts\activate.bat
pip install -q litellm feedparser requests pyyaml python-dateutil

echo ✅ 安装完成！
echo 📝 请设置 API Key: set AI_API_KEY=your-key
```

### 4. Windows 运行脚本

```bat
@echo off
REM 文件名: run.bat

cd /d "%USERPROFILE%\TheNEWs"
if exist venv\Scripts\activate.bat call venv\Scripts\activate.bat
python -m trendradar %*
```

### 5. 一键安装并运行（Linux/Mac）

```bash
#!/bin/bash
# 文件名: quick-install.sh

set -e

echo "🚀 TheNEWs 快速安装"

# 检查依赖
command -v python3 >/dev/null 2>&1 || { echo "❌ 需要 Python 3"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ 需要 Git"; exit 1; }

# 克隆
INSTALL_DIR="$HOME/TheNEWs"
[ ! -d "$INSTALL_DIR" ] && git clone https://github.com/fezeryang/TheNEWs.git "$INSTALL_DIR"

cd "$INSTALL_DIR"

# 虚拟环境
[ ! -d venv ] && python3 -m venv venv

# 安装
source venv/bin/activate
pip install -q litellm feedparser requests pyyaml python-dateutil

echo "✅ 安装完成！"
echo ""
echo "📍 设置 API Key:"
echo "   export AI_API_KEY='sk-xxxxx'"
echo ""
echo "📍 DeepSeek: https://platform.deepseek.com/api_keys"
```

### 6. 定时任务脚本（Linux/Mac）

```bash
#!/bin/bash
# 文件名: setup-cron.sh

# 添加每小时定时任务
(crontab -l 2>/dev/null | grep -v TheNEWs; echo "0 * * * * cd ~/TheNEWs && ./run.sh") | crontab -

echo "✅ 定时任务已设置（每小时运行）"
echo "查看: crontab -l"
```

### 7. 定时任务脚本（Windows）

```bat
@echo off
REM 文件名: setup-scheduled-task.bat

schtasks /create /tn "TheNEWS热点" /tr "C:\Users\%USERNAME%\TheNEWs\run.bat" /sc hourly /f
echo ✅ 定时任务已创建
```

---

## 快速开始

### 用户可直接请求 Claude：

```
用户: 帮我安装 TheNEWs
Claude: [读取 skill 中的 install.sh 脚本]
       [执行安装步骤]

用户: 运行 TheNEWS 获取热点
Claude: [读取 skill 中的 run.sh 脚本]
       [执行并返回结果]
```

---

## API Key 配置

### 获取方式

- **DeepSeek**（推荐，便宜）: https://platform.deepseek.com/api_keys
- **OpenAI**: https://platform.openai.com/api-keys

### 配置方法

```bash
# 临时（当前会话）
export AI_API_KEY="sk-xxxxx"

# 永久（添加到 ~/.bashrc）
echo 'export AI_API_KEY="sk-xxxxx"' >> ~/.bashrc
source ~/.bashrc

# Windows
set AI_API_KEY=sk-xxxxx
```

---

## 配置文件说明

默认配置文件 `~/TheNEWs/config/config.yaml`：

```yaml
# AI 模型
ai:
  model: "deepseek/deepseek-chat"
  api_key: ""  # 留空使用环境变量

# GEO 分析
ai_analysis:
  enabled: true
  mode: "geo"              # 借势营销模式
  hotspot_mode: true       # 热点模式
  hotspot_max_count: 30    # 分析30条
  language: "Chinese"

# 热点平台
platforms:
  sources:
    - {id: "weibo", name: "微博"}
    - {id: "zhihu", name: "知乎"}
    - {id: "douyin", name: "抖音"}
    - {id: "bilibili", name: "B站"}
    - {id: "baidu", name: "百度"}
```

---

## 输出位置

```
~/TheNEWs/output/
├── content/
│   ├── xiaohongshu/YYYY-MM-DD/   # 小红书笔记
│   ├── wechat/YYYY-MM-DD/        # 公众号文章
│   └── prompts/YYYY-MM-DD/       # 配图提示词
└── html/YYYY-MM-DD/              # HTML 报告
```

---

## 常用命令

```bash
# 安装
bash <(curl -s https://raw.githubusercontent.com/fezeryang/TheNEWs/master/scripts/install.sh)

# 运行
cd ~/TheNEWs && ./run.sh

# 更新
cd ~/TheNEWs && git pull && ./run.sh

# 查看日志
cd ~/TheNEWs && DEBUG=1 ./run.sh

# 查看输出
ls ~/TheNEWs/output/content/xiaohongshu/$(date +%Y-%m-%d)/
```

---

## Claude 可执行操作

当用户请求以下任务时，Claude 应使用本 skill 中的脚本：

| 用户请求 | Claude 操作 |
|---------|-----------|
| "安装 TheNEWS" | 读取并执行 install.sh/install.bat |
| "运行热点分析" | 读取并执行 run.sh/run.bat |
| "设置定时任务" | 读取并执行 setup-cron.sh/setup-scheduled-task.bat |
| "更新项目" | 执行 git pull 并重新运行 |
| "查看生成内容" | 读取 output/content/ 目录文件 |

---

*此 skill 包含所有必需脚本，Claude 可直接读取和执行*
