# GEO 分析 Docker 部署指南

本文档说明如何在 Docker 环境中启用和配置 GEO (Generative Engine Optimization) 趋势分析功能。

## 功能简介

GEO 分析系统能够将热点新闻转化为企业营销机会，通过 AI 分析提供：
- 品牌/产品实体识别
- 营销价值评分（0-100分）
- 话术转化路径生成
- 竞品分析框架
- GEO 营销推荐

## Docker 环境配置

### 1. 启用 GEO 分析

编辑 `docker/.env` 文件，配置以下环境变量：

```bash
# ============================================
# AI 配置（必须先启用）
# ============================================
AI_ANALYSIS_ENABLED=true
AI_API_KEY=your_api_key_here
AI_MODEL=deepseek/deepseek-chat

# ============================================
# GEO 分析配置
# ============================================
# 是否启用 GEO 趋势分析
GEO_ENABLED=true

# 每次最多分析的新闻数量（建议不超过20）
GEO_MAX_NEWS=10

# 最低营销价值分数（0-100，低于此分数的新闻不会生成推荐）
GEO_MIN_MARKETING_SCORE=60

# 分析语言（Chinese 或 English）
GEO_LANGUAGE=Chinese

# 输出目录（相对于 /app/output）
GEO_OUTPUT_DIR=geo_analysis

# 是否保存 JSON 结果
GEO_SAVE_JSON=true

# 是否必须包含品牌实体（true=只分析包含品牌的新闻）
GEO_REQUIRE_BRAND=true

# 实体最低热度分数（0-100）
GEO_MIN_ENTITY_SCORE=50

# 高优先级推荐分数阈值（≥80分为高优先级）
GEO_HIGH_PRIORITY_SCORE=80

# 中优先级推荐分数阈值（≥60分为中优先级）
GEO_MEDIUM_PRIORITY_SCORE=60
```

### 2. 启动容器

```bash
cd docker
docker-compose up -d
```

### 3. 查看 GEO 分析结果

GEO 分析结果保存在 `output/geo_analysis/` 目录：

```bash
# 查看输出目录
ls -lh output/geo_analysis/

# 查看最新的分析结果
cat output/geo_analysis/geo_analysis_*.json
```

## 配置说明

### 基础配置

| 环境变量 | 说明 | 默认值 | 示例 |
|---------|------|--------|------|
| `GEO_ENABLED` | 是否启用 GEO 分析 | `false` | `true` |
| `GEO_MAX_NEWS` | 每次分析的新闻数量上限 | `10` | `20` |
| `GEO_MIN_MARKETING_SCORE` | 营销价值最低分数 | `60` | `70` |
| `GEO_LANGUAGE` | 分析语言 | `Chinese` | `English` |

### 输出配置

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `GEO_OUTPUT_DIR` | 输出目录（相对路径） | `geo_analysis` |
| `GEO_SAVE_JSON` | 是否保存 JSON 结果 | `true` |

### 过滤配置

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `GEO_REQUIRE_BRAND` | 是否必须包含品牌实体 | `true` |
| `GEO_MIN_ENTITY_SCORE` | 实体最低热度分数 | `50` |

### 推荐配置

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `GEO_HIGH_PRIORITY_SCORE` | 高优先级分数阈值 | `80` |
| `GEO_MEDIUM_PRIORITY_SCORE` | 中优先级分数阈值 | `60` |

## 输出格式

GEO 分析结果以 JSON 格式保存，文件名格式：`geo_analysis_YYYYMMDD_HHMMSS.json`

示例输出：

```json
{
  "news_id": "platform_001",
  "title": "小米汽车SU7降价促销",
  "entities": [
    {
      "name": "小米汽车",
      "type": "brand",
      "hotness_score": 85,
      "mentions": 3
    }
  ],
  "marketing_value": {
    "score": 88,
    "dimensions": {
      "controversy": 70,
      "new_product": 90,
      "topic_hotness": 85
    },
    "reasons": ["价格调整", "市场竞争", "热度高"],
    "marketing_angle": "价格战"
  },
  "conversation_bridge": {
    "templates": [
      {
        "style": "市场分析",
        "hook": "小米汽车降价了...",
        "call_to_action": "我们来做一份竞品分析报告"
      }
    ]
  },
  "competitor_analysis": {
    "target_brand": "小米汽车",
    "competitors": ["特斯拉", "蔚来", "理想"],
    "comparison_dimensions": ["价格策略", "市场定位"]
  },
  "geo_recommendation": {
    "recommended": true,
    "priority": "high",
    "confidence_score": 88
  }
}
```

## 查看日志

```bash
# 查看容器日志
docker logs trendradar

# 实时查看日志
docker logs -f trendradar

# 查看最近的 GEO 分析日志
docker logs trendradar 2>&1 | grep "\[GEO\]"
```

## 性能建议

1. **控制分析数量**：
   - `GEO_MAX_NEWS` 建议设置为 10-20
   - 每条新闻需要 5 次 AI 调用，过多会增加耗时和成本

2. **选择合适的模型**：
   - 推荐使用 `deepseek/deepseek-chat` 或 `gpt-3.5-turbo`
   - 速度快、成本低、效果好

3. **调整分数阈值**：
   - 提高 `GEO_MIN_MARKETING_SCORE` 可以减少低价值分析
   - 降低阈值可以获得更多推荐，但质量可能下降

4. **定期清理输出**：
   ```bash
   # 保留最近 7 天的结果
   find output/geo_analysis/ -name "*.json" -mtime +7 -delete
   ```

## 故障排查

### GEO 分析未启动

1. 检查 AI 配置是否正确：
   ```bash
   docker exec trendradar env | grep AI_
   ```

2. 检查 GEO 配置：
   ```bash
   docker exec trendradar env | grep GEO_
   ```

3. 查看错误日志：
   ```bash
   docker logs trendradar 2>&1 | grep -A 5 "\[GEO\]"
   ```

### 常见错误

1. **"AI model or API key not configured"**
   - 解决：设置 `AI_API_KEY` 和 `AI_MODEL`

2. **"未识别到实体"**
   - 解决：降低 `GEO_MIN_ENTITY_SCORE` 或检查新闻内容质量

3. **"营销价值过低"**
   - 解决：降低 `GEO_MIN_MARKETING_SCORE` 阈值

## 与配置文件的关系

Docker 环境变量会覆盖 `config/config.yaml` 中的配置。优先级：

```
环境变量 > config.yaml
```

如果不设置环境变量，将使用 `config/config.yaml` 中的默认值。

## 更多信息

详细文档请参考项目根目录的 `GEO_README.md`。
