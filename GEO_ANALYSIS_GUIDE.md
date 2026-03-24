# GEO 借势引流分析系统使用指南

## 📖 什么是 GEO 分析

GEO（Growth through Event Opportunities）分析系统是 TrendRadar 的营销机会挖掘模式，核心目标是：

**将公共领域的热点新闻（流量）转化为企业服务（产品）的关注度**

与通用热点分析不同，GEO 模式专注于识别商业机会，帮助营销团队发现：
- 哪些热点事件可以"借势"营销
- 如何设计自然的话术转换漏斗
- 如何将"吃瓜群众"转化为"深度分析客户"

---

## 🎯 核心功能

### 1️⃣ **实体识别（Entity Recognition）**

自动识别新闻中的营销相关实体：
- **品牌**（Brand）：如"小米汽车"、"特斯拉"
- **产品**（Product）：如"SU7"、"Model 3"
- **行业**（Industry）：如"新能源汽车"、"AI 芯片"
- **人物**（Person）：如"雷军"、"马斯克"
- **技术**（Technology）：如"自动驾驶"、"大语言模型"

每个实体包含：
- 热度评分（0-100）
- 提及次数
- 行业类别
- 上下文描述

### 2️⃣ **营销价值判断（Marketing Value Assessment）**

AI 从 6 个维度评估新闻的营销潜力：

| 维度 | 说明 | 示例 |
|-----|------|------|
| **争议性** | 话题有争议、用户反感度高 | 品牌道歉事件、产品质量问题 |
| **新品发布** | 产品发布、功能更新 | 新车发布、软件升级 |
| **排名变化** | 市场份额变动、榜单排名 | 销量超越、股价暴涨 |
| **话题热度** | 传播度、病毒性、跨平台霸屏 | 全网刷屏、热搜第一 |
| **时效性** | 新闻新鲜度、是否当日热点 | 刚刚发生、正在进行 |
| **行业影响** | 对行业的长期影响力 | 政策变动、技术革命 |

**总评分规则**：
- 🔥 **80+ 分** - 高价值机会（high_opportunity）：强烈推荐做深度分析
- 📈 **50-79 分** - 中等机会（medium_opportunity）：有一定价值但需评估
- 📉 **30-49 分** - 低价值（low_opportunity）：价值较低
- ❌ **<30 分** - 不适合（not_suitable）：不适合借势营销

### 3️⃣ **逻辑桥接（Conversation Bridge）**

这是最关键的转换漏斗，设计从"看新闻/吃瓜"到"需要深度竞品分析"的自然话术：

```
Hook (勾子)
    ↓
Bridge (桥梁)
    ↓
CTA (行动召唤)
```

**示例**：

| 步骤 | 内容 | 目的 |
|-----|------|------|
| **Hook** | "小米汽车又出新招——SU7降价促销" | 直击消费者关注点，制造话题吸引力 |
| **Bridge** | "但你有没有想过，为什么它要降价？背后的战略逻辑是什么？" | 提出疑问，暴露信息缺口，升级思考层级 |
| **CTA** | "我们来做一份《小米汽车 vs 竞品策略对比报告》，看看谁的策略更高明" | 自然转化到深度分析服务需求 |

**转化概率预测**：系统会预估转化率（如"35-45%"），帮助评估营销投入回报。

### 4️⃣ **竞品对比分析（Competitor Analysis）**

基于识别的实体，自动构建竞品对比框架：
- **目标品牌**：主要分析对象
- **竞品列表**：3-5 个对标竞品
- **对比维度**：定价策略、产品差异化、营销渠道等
- **战略洞察**：2-4 条可执行的对比结论

---

## ⚙️ 配置指南

### 步骤 1：开启 GEO 模式

编辑 `config/config.yaml`：

```yaml
ai_analysis:
  enabled: true
  
  # 切换到 GEO 模式
  mode: "geo"  # 可选: "generic" | "geo"
  
  # GEO 关注领域（可选）
  # 留空则不限制领域，填写后 AI 会更关注该领域
  geo_focus: ""  # 示例: "汽车行业"、"科技产品"、"电商零售"
  
  # 使用 GEO 专用 prompt
  prompt_file: "ai_analysis_geo_prompt.txt"
  
  language: "Chinese"
  max_news_for_analysis: 50
  include_rss: false
  include_rank_timeline: true
```

### 步骤 2：配置 AI 模型

GEO 分析需要较强的推理能力，推荐使用：

```yaml
ai:
  model: "deepseek/deepseek-chat"  # 推荐：性价比高
  # model: "openai/gpt-4o"         # 备选：效果更好但成本高
  # model: "anthropic/claude-3-5-sonnet"  # 备选：推理能力强
  
  api_key: "your-api-key"  # 建议使用环境变量 AI_API_KEY
  temperature: 1.0
  max_tokens: 5000
```

### 步骤 3：配置推送渠道

GEO 分析结果会自动适配各推送渠道：

- ✅ **飞书**：支持彩色标签、层级展示
- ✅ **钉钉**：支持 Markdown 格式
- ✅ **企业微信**：支持 Markdown 格式
- ✅ **邮件**：支持 HTML 富文本格式
- ✅ **Telegram**：支持 Markdown 格式
- ✅ 其他渠道均已适配

---

## 📊 输出格式

GEO 分析会输出结构化的 JSON 数据，包含以下字段：

```json
{
  "analysis_mode": "geo",
  "entities": [
    {
      "name": "小米汽车",
      "type": "brand",
      "category": "automotive",
      "hotness_score": 85,
      "mentions": 156,
      "context": "在新闻中的上下文描述"
    }
  ],
  "marketing_value": {
    "score": 88,
    "overall_rating": "high_opportunity",
    "dimensions": {
      "controversy": 75,
      "new_product": 85,
      "ranking_change": 60,
      "topic_heat": 90,
      "timeliness": 95,
      "industry_impact": 85
    },
    "reasons": [
      "新品降价促销，成为市场热议焦点",
      "与特斯拉等竞品形成直接对标",
      "全网传播度高，跨平台霸屏"
    ]
  },
  "conversation_bridge": {
    "hook": "小米汽车又出新招——SU7降价促销",
    "bridge": "但你有没有想过，为什么它要降价？背后的战略逻辑是什么？",
    "call_to_action": "我们来做一份《小米汽车 vs 竞品策略对比报告》，看看谁的策略更高明",
    "conversion_probability": "35-45%"
  },
  "competitor_analysis": {
    "target_brand": "小米汽车",
    "identified_competitors": ["特斯拉", "比亚迪", "蔚来", "理想汽车"],
    "comparison_dimensions": ["定价策略", "产品差异化", "营销渠道", "用户基数", "技术路线"],
    "strategic_insights": [
      "小米采用降价扩容，特斯拉坚守溢价",
      "比亚迪靠产能优势压低价格"
    ]
  }
}
```

---

## 💡 使用技巧

### 1. 聚焦特定领域

如果你的业务只关注某个领域，可以设置 `geo_focus`：

```yaml
ai_analysis:
  geo_focus: "新能源汽车行业"
```

这样 AI 会优先识别该领域的实体和机会。

### 2. 提高分析质量

- **增加新闻数量**：`max_news_for_analysis: 100`（需要更多 token）
- **开启完整时间线**：`include_rank_timeline: true`（帮助 AI 判断热度趋势）
- **包含 RSS 内容**：`include_rss: true`（获取更专业的信息）

### 3. 成本控制

GEO 分析相比通用分析稍贵（因为输出更复杂），建议：

- 使用 DeepSeek（`deepseek/deepseek-chat`）：约 0.15 元/次
- 降低推送频率：从每小时 1 次改为每 2-4 小时 1 次
- 限制分析新闻数：`max_news_for_analysis: 30-50`

### 4. 过滤无效热点

并非所有热点都适合借势。GEO 系统会自动过滤：
- 纯娱乐八卦（无商业价值）
- 社会负面新闻（品牌风险高）
- 与业务无关的领域

如果营销价值评分 < 30 分，系统会标记为"不适合"。

---

## 🔄 通用模式 vs GEO 模式

| 维度 | 通用模式（generic） | GEO 模式（geo） |
|-----|-------------------|----------------|
| **目标** | 理解热点趋势 | 将热点转化为营销机会 |
| **输出** | 5大板块分析 | 4步营销转换漏斗 |
| **数据** | 高层次洞察 | 可执行商机线索 |
| **转换** | N/A | Hook→Bridge→CTA |
| **竞品** | 无 | 对标竞品分析 |
| **适用场景** | 投资者、研究员、普通用户 | 营销团队、品牌方、咨询公司 |

**何时使用 GEO 模式？**
- ✅ 你是营销团队，需要找到借势机会
- ✅ 你是咨询公司，需要生成竞品分析报告
- ✅ 你关注某个特定行业，想挖掘商业洞察
- ✅ 你想将热点转化为客户咨询需求

**何时使用通用模式？**
- ✅ 你只是想了解每天发生了什么
- ✅ 你关注多个不相关的领域
- ✅ 你不需要商业化转换
- ✅ 你想节省 token 成本

---

## 🐛 常见问题

### Q1: GEO 模式下没有输出竞品分析？

**原因**：当日新闻中可能没有明显的商业实体（如纯社会新闻）。

**解决**：
1. 检查 `entities` 数组是否为空
2. 如果营销价值评分 < 30，说明不适合借势
3. 可设置 `geo_focus` 聚焦特定领域

### Q2: 转化率预测准确吗？

**说明**：转化率是 AI 基于历史经验的估算，实际效果受多种因素影响：
- 话术设计质量
- 目标受众匹配度
- 执行时机和渠道

建议将其作为参考，而非绝对值。

### Q3: 如何自定义竞品列表？

**方法**：GEO 系统目前基于 AI 自动识别竞品。如需指定竞品，可以：
1. 在 `geo_focus` 中明确提及（如"小米汽车 vs 特斯拉"）
2. 修改 `config/ai_analysis_geo_prompt.txt` 添加自定义规则

### Q4: GEO 模式成本多少？

**估算**（基于 DeepSeek 模型）：
- 每次分析：约 0.10-0.20 元（取决于新闻数量）
- 每天 24 次推送：约 2.4-4.8 元/天
- 每月成本：约 72-144 元/月

建议根据预算调整推送频率。

---

## 📞 技术支持

遇到问题？可以通过以下方式获取帮助：

1. **GitHub Issues**：https://github.com/sansan0/TrendRadar/issues
2. **查看日志**：检查终端输出的 `[GEO]` 前缀日志
3. **调试模式**：设置 `advanced.debug: true` 查看完整 AI 输入输出

---

## 📚 更多资源

- [README.md](README.md) - 项目主文档
- [README-EN.md](README-EN.md) - English Documentation
- [config/ai_analysis_geo_prompt.txt](config/ai_analysis_geo_prompt.txt) - GEO Prompt 配置
- [config/ai_analysis_prompt.txt](config/ai_analysis_prompt.txt) - 通用模式 Prompt

---

**版本**：v5.4.0+  
**最后更新**：2026-01-23
