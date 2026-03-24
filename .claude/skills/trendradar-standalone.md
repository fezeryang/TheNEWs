---
name: trendradar-standalone
description: 热点新闻聚合与GEO借势分析 - 自动安装运行版 | Hot news aggregation with AI-powered marketing content generation
version: 1.0.0
author: fezeryang
repository: https://github.com/fezeryang/TheNEWs
license: MIT
---

# TheNEWs - 自包含安装版

不需要预先克隆项目。加载此 skill 后，Claude 将自动完成安装和运行。

---

## 安装步骤（自动执行）

### 步骤 1：获取项目

```bash
# 克隆项目到用户目录
git clone https://github.com/fezeryang/TheNEWs.git ~/TheNEWs
cd ~/TheNEWs
```

### 步骤 2：安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

**依赖列表**（如果 requirements.txt 不存在）：
```
litellm>=1.0.0
feedparser>=6.0.0
requests>=2.31.0
pyyaml>=6.0.0
python-dateutil>=2.8.0
```

### 步骤 3：配置 API Key

编辑 `~/TheNEWs/config/config.yaml`：

```yaml
ai:
  model: "deepseek/deepseek-chat"
  api_key: ""  # 必填：填写你的 API Key
  # 或使用环境变量：export AI_API_KEY=your_key
```

**获取 API Key**：
- DeepSeek: https://platform.deepseek.com/api_keys
- OpenAI: https://platform.openai.com/api-keys

---

## 运行命令

### 基础运行

```bash
cd ~/TheNEWs
python -m trendradar
```

### 热点模式（推荐）

```bash
# 直接分析热榜前30条，不依赖关键词
cd ~/TheNEWs
# 确保 config.yaml 中 hotspot_mode: true
python -m trendradar
```

### Docker 运行（无需 Python）

```bash
# 待发布镜像，或使用本地构建
docker build -t thenews:latest ~/TheNEWs
docker run --rm \
  -v ~/TheNEWs/config:/app/config \
  -v ~/TheNEWs/output:/app/output \
  -e AI_API_KEY=your_key \
  thenews:latest
```

---

## 输出位置

运行完成后，查看生成的内容：

```bash
# 小红书笔记
ls ~/TheNEWs/output/content/xiaohongshu/$(date +%Y-%m-%d)/

# 公众号文章
ls ~/TheNEWs/output/content/wechat/$(date +%Y-%m-%d)/

# 配图提示词
ls ~/TheNEWs/output/content/prompts/$(date +%Y-%m-%d)/
```

---

## 配置说明

### 热点平台配置

编辑 `config/config.yaml` 中的 `platforms.sources`：

```yaml
platforms:
  enabled: true
  sources:
    - id: "weibo"      # 微博
    - id: "zhihu"      # 知乎
    - id: "douyin"     # 抖音
    - id: "bilibili"   # B站
    - id: "toutiao"    # 今日头条
    - id: "baidu"      # 百度热搜
```

### GEO 分析配置

```yaml
ai_analysis:
  enabled: true
  mode: "geo"                    # 借势营销模式
  hotspot_mode: true             # 热点模式（不依赖关键词）
  hotspot_max_count: 30          # 分析前30条
  language: "Chinese"            # 输出语言
```

### 推送通知配置（可选）

```yaml
notification:
  enabled: true
  channels:
    feishu:
      webhook_url: "YOUR_WEBHOOK"
```

---

## 快速测试（最小配置）

1. **安装**：
```bash
git clone https://github.com/fezeryang/TheNEWs.git ~/TheNEWs
cd ~/TheNEWs
pip install litellm feedparser requests pyyaml python-dateutil
```

2. **配置**：
```bash
# 设置 API Key 环境变量
export AI_API_KEY="sk-xxxxx"
```

3. **运行**：
```bash
python -m trendradar
```

---

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| `ModuleNotFoundError` | 运行 `pip install -r requirements.txt` |
| `API Key not configured` | 设置 `AI_API_KEY` 环境变量或编辑 config.yaml |
| 爬取失败 | 检查网络连接，国内热榜可能需要代理 |
| 没有生成内容 | 检查 AI 分析是否被安全过滤，查看日志 |

---

## 定时运行

### Linux/Mac (crontab)

```bash
# 编辑 crontab
crontab -e

# 每小时运行一次
0 * * * * cd ~/TheNEWs && source venv/bin/activate && python -m trendradar
```

### Windows (Task Scheduler)

创建计划任务，每小时运行：
```
程序: ~/TheNEWs/venv/Scripts/python.exe
参数: -m trendradar
起始位置: ~/TheNEWs
```

---

## 卸载

```bash
# 删除项目目录
rm -rf ~/TheNEWs

# 如果使用了虚拟环境，它会随项目一起删除
```

---

## 更新

```bash
cd ~/TheNEWs
git pull
pip install -r requirements.txt --upgrade
```

---

*此 skill 为自包含版本，无需预先克隆 TheNEWs 项目。*
