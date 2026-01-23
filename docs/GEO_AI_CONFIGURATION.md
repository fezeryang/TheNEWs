# GEO AI 配置指南

## 概述

TrendRadar 支持两种 AI 分析模式：

1. **通用模式 (general)**：分析热点新闻趋势、情感和风险预警（默认）
2. **GEO 模式 (geo)**：识别品牌营销机会，提供借势引流方案

本文档介绍如何配置和使用 GEO 模式。

## 快速开始

### 方法 1：修改配置文件

编辑 `config/config.yaml`，找到 `ai_analysis` 部分，修改 `mode` 为 `geo`：

```yaml
ai_analysis:
  enabled: true
  mode: "geo"  # 改为 geo 模式
  language: "Chinese"
  # 其他配置...
```

### 方法 2：使用环境变量

无需修改配置文件，直接设置环境变量：

```bash
export AI_ANALYSIS_MODE=geo
```

或在 Docker 环境中：

```bash
docker run -e AI_ANALYSIS_MODE=geo ...
```

或在 GitHub Actions 中添加到 Secrets/Variables：

```
AI_ANALYSIS_MODE=geo
```

## 配置详解

### 基础配置

```yaml
ai_analysis:
  enabled: true                     # 是否启用 AI 分析
  mode: "geo"                       # 分析模式：general | geo
  language: "Chinese"               # 输出语言
  prompt_file: "ai_analysis_prompt.txt"  # 会自动切换到 ai_geo_prompt.txt
  max_news_for_analysis: 50         # 参与分析的新闻数量上限
  include_rss: false                # 是否包含 RSS 内容
  include_rank_timeline: true       # 是否包含排名时间线
```

### GEO 专用配置

```yaml
ai_analysis:
  # ... 基础配置 ...
  
  # GEO 分析专用配置
  geo:
    max_entities: 5                 # 最多识别的实体数量
    min_marketing_score: 60         # 最低营销价值分（低于此分的实体不推荐）
    brands_filter: []               # 品牌过滤列表（留空表示不过滤）
                                    # 示例: ["小米", "华为", "苹果"]
```

#### 配置说明

- **max_entities**：最多识别几个热点实体（品牌/产品/公司）
  - 建议值：3-5
  - 过多会增加 token 消耗和响应时间

- **min_marketing_score**：营销价值的最低分数线
  - 范围：0-100
  - 建议值：60（表示只推荐中等以上价值的实体）
  - 低于此分的实体仍会识别，但在推荐建议中会标记为"不推荐"

- **brands_filter**：品牌白名单过滤
  - 留空：不过滤，识别所有品牌
  - 填写列表：只关注特定品牌
  - 示例：`["小米", "华为", "苹果"]` 只识别这三个品牌

## GEO 分析输出

### 输出结构

GEO 模式的分析结果包含以下部分：

```json
{
  "geo_analysis": {
    "entities": [
      {
        "name": "小米",
        "type": "brand",
        "marketing_value": 85,
        "value_reasons": ["新品发布+30分", "价格调整+15分"],
        "hotness_score": 92
      }
    ],
    "conversation_bridge": {
      "hook": "小米新品发布引发热议...",
      "bridge": "但你知道它的真实竞争力吗？",
      "cta": "来看小米 vs 竞品的深度对比分析"
    },
    "competitor_analysis": {
      "brand": "小米",
      "competitors": ["华为", "三星", "苹果"],
      "comparison_points": ["产品创新", "定价策略", "市场占有率"]
    },
    "geo_recommendation": {
      "recommended": true,
      "priority": "high",
      "confidence": 0.92,
      "execution_plan": "...",
      "expected_outcome": "预期转化率 X%"
    }
  }
}
```

### 输出字段说明

#### 1. entities（热点实体）
- **name**：实体名称
- **type**：实体类型（brand/product/company）
- **marketing_value**：营销价值评分（0-100）
- **value_reasons**：评分理由列表
- **hotness_score**：热度评分（0-100）

#### 2. conversation_bridge（话术桥接）
- **hook**：吸引注意力的钩子
- **bridge**：引出分析必要性的桥接语
- **cta**：行动召唤

#### 3. competitor_analysis（竞品分析）
- **brand**：主品牌名称
- **competitors**：竞品列表
- **comparison_points**：对比维度
- **differentiation**：核心差异化点

#### 4. geo_recommendation（推荐建议）
- **recommended**：是否推荐（布尔值）
- **priority**：优先级（high/medium/low）
- **confidence**：信心度（0.0-1.0）
- **execution_plan**：执行计划
- **expected_outcome**：预期效果

## 通知消息示例

### 飞书/钉钉通知

```
📊 GEO 借势分析

🎯 热点实体识别

1. 小米 (brand)
   营销价值: 85/100
   热度评分: 92/100
   评分理由: 新品发布+30分, 价格调整+15分

💬 话术转换方案
Hook: 小米新品发布引发热议...
Bridge: 但你知道它的真实竞争力吗？
CTA: 来看小米 vs 竞品的深度对比分析

🔍 竞品对比框架
主品牌: 小米
竞品: 华为, 三星, 苹果
对比维度: 产品创新, 定价策略, 市场占有率

✅ GEO 推荐
推荐指数: 推荐
优先级: 🔴 HIGH
信心度: 92%
执行计划: ...
预期效果: 预期转化率 X%
```

## 自定义 Prompt

如果默认的 GEO prompt 不满足需求，可以自定义：

1. 复制 `config/ai_geo_prompt.txt` 到新文件，如 `config/my_geo_prompt.txt`
2. 修改 Prompt 内容
3. 在 `config.yaml` 中指定：

```yaml
ai_analysis:
  mode: "geo"
  prompt_file: "my_geo_prompt.txt"
```

### Prompt 可用变量

- `{language}`：输出语言
- `{report_mode}`：报告模式
- `{report_type}`：报告类型
- `{current_time}`：当前时间
- `{news_count}`：热榜新闻条数
- `{rss_count}`：RSS 新闻条数
- `{keywords}`：匹配的关键词列表
- `{platforms}`：数据来源平台列表
- `{news_content}`：热榜新闻内容
- `{rss_content}`：RSS 订阅内容

## 切换回通用模式

如需切换回通用分析模式：

### 方法 1：修改配置文件

```yaml
ai_analysis:
  mode: "general"
```

### 方法 2：环境变量

```bash
export AI_ANALYSIS_MODE=general
```

或删除该环境变量：

```bash
unset AI_ANALYSIS_MODE
```

## 常见问题

### Q1: 如何知道当前使用的是哪种模式？

查看运行日志，GEO 模式会显示：
```
[GEO] 正在进行 GEO 借势分析...
[GEO] 识别到 3 个热点实体
[GEO] - 小米 (营销价值: 85/100)
```

通用模式会显示：
```
[AI] 正在进行 AI 分析...
[AI] 分析完成
```

### Q2: 为什么识别到的实体数量少于 max_entities？

可能原因：
1. 新闻中缺少明显的品牌/产品实体
2. 识别的实体营销价值低于 `min_marketing_score`
3. AI 判断这些实体不适合借势营销

### Q3: 如何只分析特定品牌？

在 `geo.brands_filter` 中指定品牌白名单：

```yaml
ai_analysis:
  geo:
    brands_filter: ["小米", "华为", "苹果"]
```

### Q4: GEO 模式的 token 消耗如何？

GEO 模式的 token 消耗与通用模式相近，主要取决于：
- `max_news_for_analysis`：分析的新闻数量
- `include_rank_timeline`：是否包含排名时间线
- `include_rss`：是否包含 RSS 内容

建议从较小的值开始测试（如 `max_news_for_analysis: 30`）。

### Q5: 可以同时使用两种模式吗？

不可以，同一时间只能使用一种模式。如果需要同时获得两种分析，可以：
1. 分别运行两次，每次使用不同的模式
2. 或在不同的环境/实例中运行

## 最佳实践

1. **测试阶段**：
   - 先使用 `max_news_for_analysis: 20` 进行测试
   - 观察识别到的实体是否符合预期
   - 调整 `min_marketing_score` 找到合适的阈值

2. **生产环境**：
   - 设置 `max_entities: 3-5`，避免信息过载
   - `min_marketing_score: 60-70`，只推荐高价值机会
   - 使用 `brands_filter` 聚焦核心品牌

3. **成本控制**：
   - 合理设置推送频率（如每小时或每2小时）
   - 使用 `max_news_for_analysis` 限制分析范围
   - 考虑在非高峰时段运行

4. **结果利用**：
   - 将 GEO 分析结果集成到内容生产流程
   - 根据 `priority` 和 `confidence` 决定执行顺序
   - 跟踪执行效果，优化评分标准

## 技术支持

如有问题，请提交 Issue 或查看项目文档：
- GitHub: https://github.com/fezeryang/TheNEWs
- README: [主项目文档](../README.md)
