# GEO 系统完整部署指南

本文档提供 GEO (Generative Engine Optimization) 趋势分析系统的完整部署说明，包括 Docker 和非 Docker 两种部署方式。

---

## 📋 目录

1. [系统要求](#系统要求)
2. [快速开始](#快速开始)
3. [Docker 部署（推荐）](#docker-部署推荐)
4. [非 Docker 部署](#非-docker-部署)
5. [配置说明](#配置说明)
6. [验证部署](#验证部署)
7. [故障排查](#故障排查)
8. [性能优化](#性能优化)

---

## 系统要求

### 基础要求
- **Python**: 3.10 或更高版本
- **AI API**: 需要支持 LiteLLM 的 AI 服务（OpenAI、DeepSeek、Gemini 等）
- **内存**: 最低 2GB RAM
- **存储**: 至少 1GB 可用空间

### Docker 要求
- **Docker**: 20.10 或更高版本
- **Docker Compose**: 1.29 或更高版本

---

## 快速开始

### 5 分钟快速部署（Docker）

```bash
# 1. 克隆仓库（如果还没有）
git clone https://github.com/fezeryang/TheNEWs.git
cd TheNEWs

# 2. 配置环境变量
cd docker
cp .env .env.local  # 可选：创建本地配置副本
vim .env  # 或使用其他编辑器

# 3. 设置必需的配置
# 在 .env 文件中设置：
# AI_ANALYSIS_ENABLED=true
# AI_API_KEY=your_actual_api_key_here
# GEO_ENABLED=true

# 4. 启动容器
docker-compose up -d

# 5. 查看日志（确认启动成功）
docker logs -f trendradar

# 6. 查看 GEO 分析结果
ls -lh ../output/geo_analysis/
```

---

## Docker 部署（推荐）

### 步骤 1: 准备配置文件

#### 1.1 编辑 `docker/.env` 文件

```bash
cd docker
vim .env  # 或使用 nano、vi 等编辑器
```

#### 1.2 配置 AI 服务（必需）

```bash
# ============================================
# AI 配置（必须先启用 AI 才能使用 GEO）
# ============================================
AI_ANALYSIS_ENABLED=true
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx  # 替换为你的实际 API Key
AI_MODEL=deepseek/deepseek-chat     # 或 openai/gpt-4、gemini/gemini-pro
AI_API_BASE=                         # 自定义 API 端点（可选）
```

**支持的模型提供商**：
- DeepSeek: `deepseek/deepseek-chat`
- OpenAI: `openai/gpt-4`, `openai/gpt-3.5-turbo`
- Google: `gemini/gemini-pro`, `gemini/gemini-2.0-flash-exp`
- Anthropic: `anthropic/claude-3-5-sonnet-20241022`
- 国内模型: `qwen/qwen-turbo`, `glm/glm-4` 等

#### 1.3 启用 GEO 分析

```bash
# ============================================
# GEO 分析配置
# ============================================
GEO_ENABLED=true                    # 启用 GEO 分析
GEO_MAX_NEWS=10                     # 每次分析的新闻数量
GEO_MIN_MARKETING_SCORE=60          # 最低营销价值分数
GEO_LANGUAGE=Chinese                # 分析语言（Chinese 或 English）

# 输出配置
GEO_OUTPUT_DIR=geo_analysis         # 输出目录
GEO_SAVE_JSON=true                  # 保存 JSON 结果

# 过滤配置
GEO_REQUIRE_BRAND=true              # 是否必须包含品牌
GEO_MIN_ENTITY_SCORE=50             # 实体最低热度分数

# 推荐阈值
GEO_HIGH_PRIORITY_SCORE=80          # 高优先级分数阈值
GEO_MEDIUM_PRIORITY_SCORE=60        # 中优先级分数阈值
```

#### 1.4 配置运行模式（可选）

```bash
# ============================================
# 运行配置
# ============================================
CRON_SCHEDULE=*/30 * * * *          # 定时任务（每30分钟）
RUN_MODE=cron                       # cron 或 once
IMMEDIATE_RUN=true                  # 启动时立即执行一次
```

### 步骤 2: 配置新闻源

编辑 `config/config.yaml` 文件（可选，使用默认配置即可）：

```yaml
# 如果需要自定义热榜平台和 RSS 源
platforms:
  enabled: true
  sources:
    - id: "weibo"
      name: "微博"
    - id: "zhihu"
      name: "知乎"
    # 添加更多平台...

rss:
  enabled: true
  feeds:
    - id: "tech-news"
      name: "科技新闻"
      url: "https://example.com/feed.xml"
    # 添加更多 RSS 源...
```

### 步骤 3: 启动服务

#### 3.1 使用预构建镜像（推荐）

```bash
cd docker
docker-compose up -d
```

#### 3.2 本地构建镜像

```bash
cd docker
docker-compose -f docker-compose-build.yml up -d
```

### 步骤 4: 验证部署

```bash
# 查看容器状态
docker ps | grep trendradar

# 查看实时日志
docker logs -f trendradar

# 查看 GEO 分析日志
docker logs trendradar 2>&1 | grep "\[GEO\]"

# 检查输出目录
ls -lh ../output/geo_analysis/
```

### 步骤 5: 查看结果

```bash
# 列出所有 GEO 分析结果
ls -lh ../output/geo_analysis/

# 查看最新的分析结果
cat ../output/geo_analysis/geo_analysis_$(ls -t ../output/geo_analysis/ | head -1)

# 使用 jq 格式化查看（如果已安装）
cat ../output/geo_analysis/geo_analysis_*.json | jq '.'
```

---

## 非 Docker 部署

### 步骤 1: 安装依赖

```bash
# 确保使用 Python 3.10+
python --version

# 安装依赖
pip install -r requirements.txt
```

### 步骤 2: 配置文件

#### 2.1 配置 `config/config.yaml`

```yaml
# AI 配置
AI:
  MODEL: "deepseek/deepseek-chat"
  API_KEY: "your_api_key_here"
  TEMPERATURE: 0.7
  MAX_TOKENS: 3000

# AI 分析功能
ai_analysis:
  enabled: true
  language: "Chinese"

# GEO 分析配置
geo:
  enabled: true
  analysis:
    max_news: 10
    min_marketing_score: 60
    language: "Chinese"
  output:
    directory: "output/geo_analysis"
    save_json: true
  filters:
    require_brand: true
    min_entity_score: 50
  recommendation:
    high_priority_score: 80
    medium_priority_score: 60
```

### 步骤 3: 运行

```bash
# 单次运行
python -m trendradar

# 定时运行（使用 cron）
# 编辑 crontab
crontab -e

# 添加定时任务（每30分钟执行一次）
*/30 * * * * cd /path/to/TheNEWs && /usr/bin/python -m trendradar >> /var/log/trendradar.log 2>&1
```

### 步骤 4: 验证

```bash
# 查看输出目录
ls -lh output/geo_analysis/

# 查看日志（如果使用 cron）
tail -f /var/log/trendradar.log | grep "\[GEO\]"
```

---

## 配置说明

### 环境变量完整列表

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `AI_ANALYSIS_ENABLED` | 启用 AI 分析 | `false` | `true` |
| `AI_API_KEY` | AI API 密钥 | 无 | `sk-xxx...` |
| `AI_MODEL` | AI 模型 | 无 | `deepseek/deepseek-chat` |
| `GEO_ENABLED` | 启用 GEO 分析 | `false` | `true` |
| `GEO_MAX_NEWS` | 分析新闻数量 | `10` | `20` |
| `GEO_MIN_MARKETING_SCORE` | 最低营销分数 | `60` | `70` |
| `GEO_LANGUAGE` | 分析语言 | `Chinese` | `English` |
| `GEO_OUTPUT_DIR` | 输出目录 | `geo_analysis` | `my_geo_output` |
| `GEO_SAVE_JSON` | 保存 JSON | `true` | `false` |
| `GEO_REQUIRE_BRAND` | 必须含品牌 | `true` | `false` |
| `GEO_MIN_ENTITY_SCORE` | 最低实体分数 | `50` | `60` |
| `GEO_HIGH_PRIORITY_SCORE` | 高优先级阈值 | `80` | `85` |
| `GEO_MEDIUM_PRIORITY_SCORE` | 中优先级阈值 | `60` | `65` |

### 配置优先级

```
环境变量 > config.yaml
```

Docker 环境中，环境变量会覆盖 `config/config.yaml` 中的配置。

---

## 验证部署

### 检查清单

- [ ] Docker 容器正在运行
- [ ] 日志中没有错误信息
- [ ] AI API 连接正常
- [ ] GEO 分析模块加载成功
- [ ] 输出目录创建成功
- [ ] 生成了 JSON 结果文件

### 验证命令

```bash
# 1. 检查容器状态
docker ps | grep trendradar
# 期望输出: trendradar 容器状态为 Up

# 2. 检查 GEO 启动日志
docker logs trendradar 2>&1 | grep -A 5 "\[GEO\]"
# 期望输出: GEO 分析相关日志

# 3. 检查输出文件
ls -lh output/geo_analysis/
# 期望输出: 至少有一个 geo_analysis_*.json 文件

# 4. 验证 JSON 格式
cat output/geo_analysis/geo_analysis_*.json | python -m json.tool > /dev/null && echo "JSON 格式正确" || echo "JSON 格式错误"
```

### 示例输出

成功运行后，日志应显示类似以下内容：

```
[GEO] 开始 GEO (Generative Engine Optimization) 分析
[GEO] 准备分析 50 条新闻（最多分析 10 条）
[GEO]   - 步骤 1/5: 实体识别
[GEO]   - 步骤 2/5: 营销价值分析
[GEO]   - 步骤 3/5: 话术桥接生成
[GEO]   - 步骤 4/5: 竞品分析
[GEO]   - 步骤 5/5: 生成 GEO 推荐
[GEO]   ✓ 分析完成 (推荐: true, 优先级: high)
[GEO] ✓ 结果已保存: /app/output/geo_analysis/geo_analysis_20260123_123456.json
[GEO] 🔥 发现 3 个高优先级营销机会
```

---

## 故障排查

### 常见问题

#### 1. GEO 分析未启动

**症状**: 日志中没有 `[GEO]` 相关信息

**解决方法**:
```bash
# 检查配置
docker exec trendradar env | grep GEO_ENABLED
# 应该显示: GEO_ENABLED=true

docker exec trendradar env | grep AI_API_KEY
# 应该显示你的 API Key

# 如果配置不正确，重新编辑 .env 并重启容器
vim docker/.env
docker-compose restart
```

#### 2. AI API 连接失败

**症状**: 错误信息 "API key not configured" 或连接超时

**解决方法**:
```bash
# 1. 验证 API Key
docker exec trendradar env | grep AI_API_KEY

# 2. 测试 API 连接（手动）
docker exec -it trendradar python -c "
import os
from trendradar.ai.client import AIClient
client = AIClient({'MODEL': os.getenv('AI_MODEL'), 'API_KEY': os.getenv('AI_API_KEY')})
result = client.chat([{'role': 'user', 'content': 'Hello'}])
print('API 连接成功:', result[:50])
"
```

#### 3. 未识别到实体

**症状**: 日志显示 "未识别到实体，跳过该新闻"

**解决方法**:
- 降低 `GEO_MIN_ENTITY_SCORE` 阈值
- 设置 `GEO_REQUIRE_BRAND=false` 允许分析无品牌新闻
- 检查新闻内容是否包含有效信息

#### 4. 营销价值过低

**症状**: 大量新闻被标记为 "营销价值过低"

**解决方法**:
```bash
# 降低阈值
GEO_MIN_MARKETING_SCORE=50  # 从 60 降至 50
```

#### 5. 输出文件权限问题

**症状**: 无法写入 output 目录

**解决方法**:
```bash
# 检查目录权限
ls -ld output/geo_analysis/

# 修复权限（在主机上）
chmod 777 output/geo_analysis/

# 或在 Docker 中
docker exec trendradar mkdir -p /app/output/geo_analysis
```

### 调试模式

启用详细日志：

```bash
# 在 docker/.env 中添加
DEBUG=true

# 重启容器
docker-compose restart

# 查看详细日志
docker logs -f trendradar
```

---

## 性能优化

### 1. 控制分析数量

```bash
# 减少每次分析的新闻数量以降低 API 成本和耗时
GEO_MAX_NEWS=5  # 从 10 减至 5
```

### 2. 选择快速模型

```bash
# 使用更快的模型
AI_MODEL=deepseek/deepseek-chat     # 快速且便宜
# AI_MODEL=openai/gpt-3.5-turbo     # 备选方案
# AI_MODEL=gemini/gemini-2.0-flash-exp  # 极快
```

### 3. 调整分析阈值

```bash
# 提高阈值以减少低价值分析
GEO_MIN_MARKETING_SCORE=70          # 从 60 提高到 70
GEO_MIN_ENTITY_SCORE=60             # 从 50 提高到 60
```

### 4. 定期清理旧数据

```bash
# 创建清理脚本
cat > cleanup_geo.sh << 'EOF'
#!/bin/bash
# 保留最近 7 天的 GEO 分析结果
find output/geo_analysis/ -name "geo_analysis_*.json" -mtime +7 -delete
echo "清理完成: $(date)"
EOF

chmod +x cleanup_geo.sh

# 添加到 crontab（每天凌晨 2 点执行）
echo "0 2 * * * /path/to/cleanup_geo.sh" | crontab -
```

### 5. 资源限制（Docker）

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  trendradar:
    # ...其他配置...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 高级配置

### 使用自定义 AI 端点

```bash
# 使用代理或自托管 API
AI_API_BASE=https://your-proxy.com/v1
AI_MODEL=openai/gpt-4
```

### 多语言部署

```bash
# 英文分析
GEO_LANGUAGE=English

# 或在 config.yaml 中配置
geo:
  analysis:
    language: "English"
```

### 自定义输出目录

```bash
# 更改输出位置
GEO_OUTPUT_DIR=custom_geo_output

# 输出将保存到: output/custom_geo_output/
```

---

## 下一步

部署成功后，你可以：

1. **查看文档**: 阅读 `GEO_README.md` 了解系统详细功能
2. **运行测试**: 使用 `test_geo_system.py` 验证所有模块
3. **查看示例**: 运行 `example_geo_usage.py` 学习 API 使用
4. **集成到工作流**: 将 GEO 分析结果集成到你的营销工作流中

---

## 获取帮助

- **文档**: 
  - `GEO_README.md` - 系统详细文档
  - `docker/GEO_DOCKER_README.md` - Docker 专用指南
  - `IMPLEMENTATION_SUMMARY.md` - 技术实现总结

- **问题报告**: 
  - GitHub Issues: https://github.com/fezeryang/TheNEWs/issues

- **测试脚本**:
  - `test_geo_system.py` - 完整测试套件
  - `example_geo_usage.py` - 使用示例

---

## 许可证

与 TrendRadar 主项目相同

---

**部署完成！开始使用 GEO 趋势分析系统吧！** 🚀
