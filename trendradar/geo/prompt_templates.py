# coding=utf-8
"""
AI Prompt 模板管理模块

统一管理 GEO 分析系统中所有 AI 分析的 Prompt 指令
支持多语言（中文/英文）和按场景分类
"""

from typing import Dict, List


class PromptTemplates:
    """Prompt 模板管理器"""

    # ===== 实体识别 Prompts =====
    ENTITY_EXTRACTION_CN = """你是一个专业的品牌和产品分析专家。请从以下新闻内容中识别所有品牌、产品、公司、行业和关键人物等营销相关实体。

新闻内容：
{content}

请输出 JSON 格式，包含以下信息：
{{
    "entities": [
        {{
            "name": "实体名称",
            "type": "brand/product/person/industry/company",
            "context": "在新闻中出现的上下文",
            "hotness_score": 0-100分的热度评分,
            "mentions": 在新闻中被提及的次数
        }}
    ]
}}

注意：
1. 不依赖预设关键词，基于文本分析识别
2. hotness_score 综合考虑：提及频次、上下文重要性、话题性
3. 只输出有营销价值的实体（排除通用词汇）
4. 返回合法的 JSON 格式"""

    ENTITY_EXTRACTION_EN = """You are a professional brand and product analysis expert. Please identify all brands, products, companies, industries, and key people from the following news content that are relevant for marketing.

News Content:
{content}

Please output in JSON format with the following information:
{{
    "entities": [
        {{
            "name": "entity name",
            "type": "brand/product/person/industry/company",
            "context": "context in which it appears in the news",
            "hotness_score": "score from 0-100",
            "mentions": "number of times mentioned in the news"
        }}
    ]
}}

Notes:
1. Do not rely on preset keywords, identify based on text analysis
2. hotness_score considers: mention frequency, context importance, topic relevance
3. Only output entities with marketing value (exclude generic terms)
4. Return valid JSON format"""

    # ===== 营销价值判断 Prompts =====
    MARKETING_VALUE_CN = """你是一个营销价值分析专家。请分析以下新闻是否具备"营销爆点"特质，并给出评分。

新闻标题：{title}
新闻内容：{content}
识别的实体：{entities}

请评估以下维度：
1. 争议性：是否有争议话题或对立观点
2. 新品发布：是否涉及新产品、新技术、新策略
3. 排名变化：是否有市场地位、排名、份额变化
4. 话题热度：社交媒体讨论度、公众关注度
5. 时效性：新闻的时效性和紧迫性
6. 行业影响：对行业的影响力和重要性

输出 JSON 格式：
{{
    "score": 0-100的总分,
    "dimensions": {{
        "controversy": 0-100,
        "new_product": 0-100,
        "ranking_change": 0-100,
        "topic_hotness": 0-100,
        "timeliness": 0-100,
        "industry_impact": 0-100
    }},
    "reasons": ["原因1", "原因2", "原因3"],
    "marketing_angle": "建议的营销切入角度",
    "target_audience": "目标受众群体"
}}

只返回合法的 JSON 格式，不要有其他内容。"""

    MARKETING_VALUE_EN = """You are a marketing value analysis expert. Please analyze whether the following news has "marketing hotspot" characteristics and provide a score.

News Title: {title}
News Content: {content}
Identified Entities: {entities}

Please evaluate the following dimensions:
1. Controversy: presence of controversial topics or opposing viewpoints
2. New Product Launch: involvement of new products, technologies, or strategies
3. Ranking Changes: changes in market position, rankings, or market share
4. Topic Hotness: social media discussion level, public attention
5. Timeliness: timeliness and urgency of the news
6. Industry Impact: influence and importance to the industry

Output in JSON format:
{{
    "score": "total score from 0-100",
    "dimensions": {{
        "controversy": "0-100",
        "new_product": "0-100",
        "ranking_change": "0-100",
        "topic_hotness": "0-100",
        "timeliness": "0-100",
        "industry_impact": "0-100"
    }},
    "reasons": ["reason1", "reason2", "reason3"],
    "marketing_angle": "suggested marketing angle",
    "target_audience": "target audience group"
}}

Return only valid JSON format with no other content."""

    # ===== 话术桥接 Prompts =====
    CONVERSATION_BRIDGE_CN = """你是一个文案专家，擅长设计从"吃瓜/看新闻"到"需要做深度竞品分析报告"的转化路径。

新闻信息：
标题：{title}
内容摘要：{summary}
关键品牌：{brand}
营销价值：{marketing_value}

请设计一套话术转换路径，包含三个部分：
1. Hook（钩子）：吸引眼球的开场，让人想继续了解
2. Bridge（桥接）：自然过渡，引导思考
3. Call-to-Action（行动召唤）：引导到 GEO 竞品分析需求

要求：
- 符合用户心理预期，自然不突兀
- 多准备 3 套不同风格的话术（技术对标、市场分析、用户决策）
- 语言要生动、有吸引力

输出 JSON 格式：
{{
    "templates": [
        {{
            "style": "技术对标/市场分析/用户决策",
            "hook": "开场钩子",
            "bridge": "桥接过渡",
            "call_to_action": "行动召唤",
            "full_text": "完整话术"
        }}
    ]
}}

只返回合法的 JSON 格式。"""

    CONVERSATION_BRIDGE_EN = """You are a copywriting expert skilled at designing conversion paths from "reading news" to "needing a deep competitive analysis report."

News Information:
Title: {title}
Summary: {summary}
Key Brand: {brand}
Marketing Value: {marketing_value}

Please design a conversion path with three parts:
1. Hook: Eye-catching opening to attract attention
2. Bridge: Natural transition to guide thinking
3. Call-to-Action: Guide to GEO competitive analysis needs

Requirements:
- Align with user psychology, natural and not abrupt
- Prepare 3 different style templates (technical benchmarking, market analysis, user decision-making)
- Language should be vivid and attractive

Output in JSON format:
{{
    "templates": [
        {{
            "style": "technical benchmarking/market analysis/user decision-making",
            "hook": "opening hook",
            "bridge": "bridge transition",
            "call_to_action": "call to action",
            "full_text": "complete script"
        }}
    ]
}}

Return only valid JSON format."""

    # ===== 竞品分析 Prompts =====
    COMPETITOR_ANALYSIS_CN = """你是一个市场竞品分析专家。基于识别出的品牌，请分析其主要竞争对手并生成对比框架。

目标品牌：{brand}
行业背景：{industry}
新闻上下文：{context}

请完成以下分析：
1. 识别 3-5 个主要竞品
2. 列出关键对比维度（产品、价格、市场、营销等）
3. 说明为什么这些竞品值得分析
4. 提供 GEO 报告的应用价值

输出 JSON 格式：
{{
    "target_brand": "目标品牌",
    "competitors": [
        {{
            "name": "竞品名称",
            "reason": "选择原因",
            "market_position": "市场定位"
        }}
    ],
    "comparison_dimensions": [
        {{
            "dimension": "对比维度名称",
            "description": "为什么这个维度重要",
            "analysis_points": ["分析点1", "分析点2"]
        }}
    ],
    "geo_value": "说明这份竞品分析对 GEO 营销的价值",
    "recommended_report_structure": ["建议的报告章节1", "章节2", "章节3"]
}}

只返回合法的 JSON 格式。"""

    COMPETITOR_ANALYSIS_EN = """You are a market competitive analysis expert. Based on the identified brand, please analyze its main competitors and generate a comparison framework.

Target Brand: {brand}
Industry Background: {industry}
News Context: {context}

Please complete the following analysis:
1. Identify 3-5 main competitors
2. List key comparison dimensions (product, price, market, marketing, etc.)
3. Explain why these competitors are worth analyzing
4. Provide application value for GEO reports

Output in JSON format:
{{
    "target_brand": "target brand",
    "competitors": [
        {{
            "name": "competitor name",
            "reason": "reason for selection",
            "market_position": "market position"
        }}
    ],
    "comparison_dimensions": [
        {{
            "dimension": "dimension name",
            "description": "why this dimension matters",
            "analysis_points": ["point1", "point2"]
        }}
    ],
    "geo_value": "explain the value of this competitive analysis for GEO marketing",
    "recommended_report_structure": ["recommended chapter 1", "chapter 2", "chapter 3"]
}}

Return only valid JSON format."""

    # ===== GEO 推荐引擎 Prompts =====
    GEO_RECOMMENDATION_CN = """你是一个 GEO（生成式引擎优化）策略专家。基于以上分析，生成完整的 GEO 推荐方案。

新闻信息：{news_info}
实体分析：{entities}
营销价值：{marketing_value}
话术路径：{conversation_bridge}
竞品分析：{competitor_analysis}

请生成完整的 GEO 推荐方案，包括：
1. 是否推荐为 GEO 营销机会
2. 执行计划（内容策略、发布渠道、时间窗口）
3. 预期效果（潜在线索、关注度提升）
4. 内容切入角度
5. 风险提示

输出 JSON 格式：
{{
    "recommended": true/false,
    "confidence_score": 0-100,
    "priority": "high/medium/low",
    "execution_plan": {{
        "content_strategy": "内容策略描述",
        "channels": ["渠道1", "渠道2"],
        "timing": "最佳发布时机",
        "key_messages": ["核心信息1", "核心信息2"]
    }},
    "expected_results": {{
        "potential_leads": "预期线索量级",
        "attention_boost": "预期关注度提升",
        "conversion_path": "转化路径描述"
    }},
    "content_angles": ["角度1", "角度2", "角度3"],
    "risks": ["风险1", "风险2"],
    "next_steps": ["步骤1", "步骤2", "步骤3"]
}}

只返回合法的 JSON 格式。"""

    GEO_RECOMMENDATION_EN = """You are a GEO (Generative Engine Optimization) strategy expert. Based on the above analysis, generate a complete GEO recommendation plan.

News Information: {news_info}
Entity Analysis: {entities}
Marketing Value: {marketing_value}
Conversation Bridge: {conversation_bridge}
Competitor Analysis: {competitor_analysis}

Please generate a complete GEO recommendation plan, including:
1. Whether to recommend as a GEO marketing opportunity
2. Execution plan (content strategy, channels, timing window)
3. Expected results (potential leads, attention boost)
4. Content angles
5. Risk warnings

Output in JSON format:
{{
    "recommended": "true/false",
    "confidence_score": "0-100",
    "priority": "high/medium/low",
    "execution_plan": {{
        "content_strategy": "content strategy description",
        "channels": ["channel1", "channel2"],
        "timing": "optimal release timing",
        "key_messages": ["key message 1", "key message 2"]
    }},
    "expected_results": {{
        "potential_leads": "expected lead volume",
        "attention_boost": "expected attention boost",
        "conversion_path": "conversion path description"
    }},
    "content_angles": ["angle1", "angle2", "angle3"],
    "risks": ["risk1", "risk2"],
    "next_steps": ["step1", "step2", "step3"]
}}

Return only valid JSON format."""

    @classmethod
    def get_prompt(cls, task: str, language: str = "Chinese") -> str:
        """
        获取指定任务和语言的 Prompt

        Args:
            task: 任务类型 (entity_extraction, marketing_value, conversation_bridge, 
                  competitor_analysis, geo_recommendation)
            language: 语言 (Chinese/English)

        Returns:
            str: Prompt 模板字符串
        """
        prompt_map = {
            "entity_extraction": {
                "Chinese": cls.ENTITY_EXTRACTION_CN,
                "English": cls.ENTITY_EXTRACTION_EN,
            },
            "marketing_value": {
                "Chinese": cls.MARKETING_VALUE_CN,
                "English": cls.MARKETING_VALUE_EN,
            },
            "conversation_bridge": {
                "Chinese": cls.CONVERSATION_BRIDGE_CN,
                "English": cls.CONVERSATION_BRIDGE_EN,
            },
            "competitor_analysis": {
                "Chinese": cls.COMPETITOR_ANALYSIS_CN,
                "English": cls.COMPETITOR_ANALYSIS_EN,
            },
            "geo_recommendation": {
                "Chinese": cls.GEO_RECOMMENDATION_CN,
                "English": cls.GEO_RECOMMENDATION_EN,
            },
        }

        if task not in prompt_map:
            raise ValueError(f"Unknown task: {task}")

        if language not in prompt_map[task]:
            # 默认使用中文
            language = "Chinese"

        return prompt_map[task][language]

    @classmethod
    def format_prompt(cls, task: str, language: str = "Chinese", **kwargs) -> str:
        """
        格式化 Prompt（填充变量）

        Args:
            task: 任务类型
            language: 语言
            **kwargs: 用于填充模板的变量

        Returns:
            str: 格式化后的 Prompt
        """
        template = cls.get_prompt(task, language)
        return template.format(**kwargs)
