# GEO 趋势分析系统文档

## 概述

GEO (Generative Engine Optimization) 趋势分析系统是一个将热点新闻转化为企业 GEO 服务营销机会的智能分析工具。系统通过 AI 分析热点新闻中的品牌/产品信息，评估营销价值，并生成从"看新闻"到"需要竞品分析报告"的转化路径。

## 核心功能

### 1. 实体识别 (Entity Extraction)
- **功能**：自动识别新闻中的品牌、产品、公司、行业、人物等营销相关实体
- **特点**：
  - 不依赖预设关键词，基于 NLP 文本分析
  - 为每个实体评估热度分数（0-100分）
  - 统计实体在新闻中的提及次数
- **模块**：`trendradar/geo/entity_extractor.py`

### 2. 营销价值分析 (Marketing Value Analysis)
- **功能**：判断新闻是否具备"营销爆点"特质并评分
- **评分维度**：
  - 争议性 (Controversy)
  - 新品发布 (New Product)
  - 排名变化 (Ranking Change)
  - 话题热度 (Topic Hotness)
  - 时效性 (Timeliness)
  - 行业影响 (Industry Impact)
- **输出**：0-100分的总分及各维度分数、判定理由
- **模块**：`trendradar/geo/marketing_value_analyzer.py`

### 3. 话术桥接 (Conversation Bridge)
- **功能**：设计从"吃瓜/看新闻"到"需要深度竞品分析报告"的转化路径
- **结构**：
  - Hook（钩子）：吸引眼球的开场
  - Bridge（桥接）：自然过渡，引导思考
  - Call-to-Action（行动召唤）：引导到 GEO 竞品分析需求
- **风格**：提供多套话术模板（技术对标、市场分析、用户决策）
- **模块**：`trendradar/geo/conversation_bridge.py`

### 4. 竞品分析 (Competitor Analysis)
- **功能**：基于识别出的品牌，自动分析竞品并生成对比框架
- **输出**：
  - 3-5个主要竞品及选择原因
  - 关键对比维度（产品、价格、市场、营销等）
  - 对比分析要点
  - GEO 报告应用价值
- **模块**：`trendradar/geo/competitor_analysis.py`

### 5. GEO 推荐引擎 (GEO Recommendation Engine)
- **功能**：综合所有分析模块，生成完整的 GEO 推荐方案
- **输出**：
  - 是否推荐为营销机会
  - 优先级（high/medium/low）
  - 执行计划（内容策略、渠道、时机）
  - 预期效果（潜在线索、关注度提升）
  - 风险提示和后续步骤
- **模块**：`trendradar/geo/geo_recommendation_engine.py`

### 6. Prompt 模板管理 (Prompt Templates)
- **功能**：统一管理所有 AI 分析的 Prompt 指令
- **特点**：
  - 支持中英文双语
  - 按场景分类（实体识别、价值判断、话术生成等）
  - 易于维护和优化
- **模块**：`trendradar/geo/prompt_templates.py`

## 系统架构

```
trendradar/geo/
├── __init__.py                        # 包初始化
├── prompt_templates.py                # AI Prompt 模板管理
├── entity_extractor.py                # 实体识别模块
├── marketing_value_analyzer.py        # 营销价值分析模块
├── conversation_bridge.py             # 话术桥接模块
├── competitor_analysis.py             # 竞品分析模块
└── geo_recommendation_engine.py       # GEO 推荐引擎（主引擎）
```

## 使用方法

### 1. 配置

在 `config/config.yaml` 中启用 GEO 分析：

```yaml
geo:
  enabled: true                          # 启用 GEO 分析
  
  analysis:
    max_news: 10                         # 每次最多分析的新闻数量
    min_marketing_score: 60              # 最低营销价值分数
    language: "Chinese"                  # 分析语言
    
  output:
    directory: "output/geo_analysis"     # 输出目录
    save_json: true                      # 保存 JSON 结果
    
  filters:
    require_brand: true                  # 必须包含品牌实体
    min_entity_score: 50                 # 实体最低热度分数
```

### 2. 与主程序集成

GEO 分析已集成到 TrendRadar 主程序中，只需启用配置即可：

```bash
python -m trendradar
```

系统会在完成热点新闻爬取和分析后，自动执行 GEO 分析流程。

### 3. 独立使用

也可以独立使用 GEO 模块：

```python
from trendradar.ai.client import AIClient
from trendradar.geo import GEORecommendationEngine

# 配置 AI 客户端
ai_config = {
    "MODEL": "deepseek/deepseek-chat",
    "API_KEY": "your_api_key",
    "TEMPERATURE": 0.7,
    "MAX_TOKENS": 3000,
}
ai_client = AIClient(ai_config)

# 创建 GEO 推荐引擎
engine = GEORecommendationEngine(
    ai_client=ai_client,
    language="Chinese",
    output_dir="output/geo_analysis",
)

# 准备新闻数据
news = {
    "id": "news_001",
    "title": "西贝莜面村推出新品莜面套餐",
    "content": "西贝莜面村今日宣布推出全新莜面套餐系列...",
    "url": "https://example.com/news",
}

# 分析单条新闻
result = engine.analyze_news(news)

# 或批量分析
news_list = [news1, news2, news3]
results = engine.analyze_news_batch(news_list, max_news=10)

# 保存结果
engine.save_results(results)

# 获取高优先级推荐
high_priority = engine.get_high_priority_recommendations(results)
```

### 4. 测试脚本

使用提供的测试脚本验证系统功能：

```bash
# 设置 API Key
export AI_API_KEY=your_api_key

# 可选：设置模型
export AI_MODEL=deepseek/deepseek-chat

# 运行测试
python test_geo_system.py
```

## 输出格式

GEO 分析结果以 JSON 格式保存，示例：

```json
{
  "news_id": "test_001",
  "title": "西贝莜面村推出新品",
  "url": "https://example.com/news",
  "analyzed_at": "2024-01-23T12:00:00",
  
  "entities": [
    {
      "name": "西贝莜面村",
      "type": "brand",
      "hotness_score": 85,
      "mentions": 3,
      "context": "西贝莜面村推出新品..."
    }
  ],
  
  "marketing_value": {
    "score": 88,
    "dimensions": {
      "controversy": 60,
      "new_product": 95,
      "ranking_change": 70,
      "topic_hotness": 85,
      "timeliness": 90,
      "industry_impact": 75
    },
    "reasons": ["新品发布", "社交热度高", "用户讨论活跃"],
    "marketing_angle": "创新升级",
    "target_audience": "年轻消费者"
  },
  
  "conversation_bridge": {
    "templates": [
      {
        "style": "技术对标",
        "hook": "西贝莜面村又出新品了，这次真的有点意思...",
        "bridge": "但你有没有想过，它为什么能这样快地推新品？",
        "call_to_action": "我们来做一份西贝 vs 竞品的深度分析报告",
        "full_text": "..."
      }
    ]
  },
  
  "competitor_analysis": {
    "target_brand": "西贝莜面村",
    "competitors": [
      {
        "name": "海底捞",
        "reason": "火锅餐饮领导者",
        "market_position": "高端火锅连锁"
      }
    ],
    "comparison_dimensions": [
      {
        "dimension": "新品策略",
        "description": "产品创新和上市速度",
        "analysis_points": ["产品研发能力", "市场反应速度"]
      }
    ],
    "geo_value": "可用于制定竞争分析报告，帮助企业制定差异化营销策略"
  },
  
  "geo_recommendation": {
    "recommended": true,
    "confidence_score": 85,
    "priority": "high",
    "execution_plan": {
      "content_strategy": "基于新品发布制作对比分析",
      "channels": ["社交媒体", "行业论坛"],
      "timing": "24小时内",
      "key_messages": ["产品创新", "竞争优势"]
    },
    "expected_results": {
      "potential_leads": "中等到高",
      "attention_boost": "显著",
      "conversion_path": "新闻关注 -> GEO 报告 -> 服务咨询"
    },
    "content_angles": ["产品对比", "市场分析"],
    "risks": ["时效性风险"],
    "next_steps": ["制作内容", "多渠道发布", "数据跟踪"]
  }
}
```

## 技术要点

### AI 模型支持

系统基于 LiteLLM，支持 100+ AI 提供商：
- OpenAI (gpt-4, gpt-3.5-turbo)
- DeepSeek (deepseek-chat, deepseek-coder)
- Anthropic Claude
- Google Gemini
- 国内模型（通义千问、文心一言等）

### 最佳实践

1. **API Key 配置**：确保在 `config/config.yaml` 中正确配置 AI 模型和 API Key
2. **新闻数量控制**：建议设置 `max_news` 不超过 20，避免 API 调用成本过高
3. **分数阈值调整**：根据实际需求调整 `min_marketing_score` 和 `min_entity_score`
4. **语言设置**：根据目标市场选择 `language`（Chinese/English）
5. **结果保存**：定期清理 `output/geo_analysis` 目录中的历史结果

### 性能考虑

- 每条新闻的完整分析需要 5 次 AI 调用（实体识别、营销价值、话术桥接、竞品分析、推荐生成）
- 建议使用快速模型（如 gpt-3.5-turbo、deepseek-chat）以降低延迟
- 批量分析时，系统会按顺序处理，避免并发调用导致的速率限制

## 扩展开发

### 添加新的分析维度

1. 在 `prompt_templates.py` 中添加新的 Prompt 模板
2. 创建新的分析模块（参考现有模块结构）
3. 在 `geo_recommendation_engine.py` 中集成新模块
4. 更新配置文件和文档

### 自定义 Prompt

所有 AI Prompt 集中在 `prompt_templates.py` 中，可以根据业务需求自定义：

```python
# 修改实体识别的 Prompt
ENTITY_EXTRACTION_CN = """
你的自定义 Prompt 内容...
{content}  # 保留变量占位符
"""
```

### 添加新的输出格式

在 `geo_recommendation_engine.py` 中的 `save_results` 方法中添加新的格式支持：

```python
def save_results(self, results, format="json"):
    if format == "json":
        # 现有的 JSON 保存逻辑
        pass
    elif format == "csv":
        # 添加 CSV 保存逻辑
        pass
```

## 故障排查

### 常见问题

1. **"未配置 AI 模型"错误**
   - 检查 `config/config.yaml` 中的 `AI` 配置
   - 确保 `MODEL` 和 `API_KEY` 已正确设置

2. **"AI 返回格式错误"**
   - AI 模型可能返回非 JSON 格式
   - 尝试更换模型或调整 Prompt
   - 检查 `debug` 模式下的原始响应

3. **"未识别到实体"**
   - 新闻内容可能不包含明显的品牌/产品信息
   - 降低 `min_entity_score` 阈值
   - 检查 Prompt 是否适合当前语言和领域

4. **分析速度慢**
   - 使用更快的 AI 模型
   - 减少 `max_news` 数量
   - 考虑并行处理（需自行实现）

## 更新日志

### v1.0.0 (2024-01-23)
- ✅ 实现实体识别模块
- ✅ 实现营销价值分析模块
- ✅ 实现话术桥接模块
- ✅ 实现竞品分析模块
- ✅ 实现 GEO 推荐引擎
- ✅ 实现 Prompt 模板管理
- ✅ 集成到主程序工作流
- ✅ 添加配置文件支持
- ✅ 创建测试脚本

## 许可证

与 TrendRadar 主项目相同

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过项目 Issue 反馈。
