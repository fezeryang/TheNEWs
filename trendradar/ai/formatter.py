# coding=utf-8
"""
AI 分析结果格式化模块

将 AI 分析结果格式化为各推送渠道的样式
"""

import html as html_lib
import re
from .analyzer import AIAnalysisResult


def _escape_html(text: str) -> str:
    """转义 HTML 特殊字符，防止 XSS 攻击"""
    return html_lib.escape(text) if text else ""


def _format_list_content(text: str) -> str:
    """
    格式化列表内容，确保序号前有换行
    例如将 "1. xxx 2. yyy" 转换为:
    1. xxx
    2. yyy
    """
    if not text:
        return ""
    
    # 去除首尾空白，防止 AI 返回的内容开头就有换行导致显示空行
    text = text.strip()
    
    # 1. 规范化：确保 "1." 后面有空格
    result = re.sub(r'(\d+)\.([^ \d])', r'\1. \2', text)

    # 2. 强制换行：匹配 "数字."，且前面不是换行符
    result = re.sub(r'(?<=[^\n])\s+(\d+\.)', r'\n\1', result)
    
    # 3. 处理 "1.**粗体**" 这种情况（虽然 Prompt 要求不输出 Markdown，但防御性处理）
    result = re.sub(r'(?<=[^\n])(\d+\.\*\*)', r'\n\1', result)

    # 4. 处理中文标点后的换行
    result = re.sub(r'([：:;,。；，])\s*(\d+\.)', r'\1\n\2', result)

    # 5. 处理 "XX方面："、"XX领域：" 等子标题换行
    # 只有在中文标点（句号、逗号、分号等）后才触发换行，避免破坏 "1. XX领域：" 格式
    result = re.sub(r'([。！？；，、])\s*([a-zA-Z0-9\u4e00-\u9fa5]+(方面|领域)[:：])', r'\1\n\2', result)

    # 6. 处理 "【XX】："(如【宏观主线】：) 前的换行，确保视觉分隔
    result = re.sub(r'(?<=[^\n])\s*(【[^】]+】[:：])', r'\n\n\1', result)

    # 7. 在列表项之间增加视觉空行（将 \n数字. 替换为 \n\n数字.）
    # 但排除标题行（以冒号结尾）之后的情况，避免标题和第一项之间有空行
    # (?<![:：]) 是负向后瞻，表示前面不能是冒号
    result = re.sub(r'(?<![:：])\n(\d+\.)', r'\n\n\1', result)

    return result


def _render_geo_analysis_markdown(geo_data: dict) -> str:
    """渲染 GEO 分析为 Markdown 格式"""
    lines = ["**🎯 GEO 营销机会分析**", ""]
    
    # 营销价值评估
    marketing_value = geo_data.get("marketing_value", {})
    score = marketing_value.get("score", 0)
    rating = marketing_value.get("overall_rating", "")
    
    rating_emoji = {"high_opportunity": "🔥", "medium_opportunity": "📈", "low_opportunity": "📉", "not_suitable": "❌"}
    emoji = rating_emoji.get(rating, "📊")
    
    lines.append(f"**营销价值评分**: {emoji} {score}/100 ({rating})")
    lines.append("")
    
    # 识别实体
    entities = geo_data.get("entities", [])
    if entities:
        lines.append("**📍 关键实体**")
        for entity in entities[:5]:  # 最多显示 5 个
            name = entity.get("name", "")
            entity_type = entity.get("type", "")
            hotness = entity.get("hotness_score", 0)
            lines.append(f"  • {name} ({entity_type}) - 热度: {hotness}")
        lines.append("")
    
    # 转换桥梁
    bridge = geo_data.get("conversation_bridge", {})
    if bridge:
        lines.append("**💡 营销话术转换**")
        hook = bridge.get("hook", "")
        bridge_text = bridge.get("bridge", "")
        cta = bridge.get("call_to_action", "")
        
        if hook:
            lines.append(f"勾子: {hook}")
        if bridge_text:
            lines.append(f"桥梁: {bridge_text}")
        if cta:
            lines.append(f"行动: {cta}")
        lines.append("")
    
    # 竞品分析
    competitor = geo_data.get("competitor_analysis", {})
    if competitor:
        target = competitor.get("target_brand", "")
        competitors = competitor.get("identified_competitors", [])
        
        if target:
            lines.append(f"**🏆 竞品对标**: {target}")
            if competitors:
                lines.append(f"竞品: {', '.join(competitors[:5])}")
            lines.append("")
    
    return "\n".join(lines)


def _render_geo_analysis_feishu(geo_data: dict) -> str:
    """渲染 GEO 分析为飞书格式"""
    lines = ["**🎯 GEO 营销机会分析**", ""]
    
    # 营销价值评估
    marketing_value = geo_data.get("marketing_value", {})
    score = marketing_value.get("score", 0)
    rating = marketing_value.get("overall_rating", "")
    reasons = marketing_value.get("reasons", [])
    
    rating_map = {
        "high_opportunity": "<font color='red'>🔥 高价值机会</font>",
        "medium_opportunity": "<font color='orange'>📈 中等机会</font>",
        "low_opportunity": "<font color='grey'>📉 低价值</font>",
        "not_suitable": "<font color='grey'>❌ 不适合</font>"
    }
    rating_text = rating_map.get(rating, rating)
    
    lines.append(f"**营销价值**: {rating_text} ({score}/100)")
    if reasons:
        for reason in reasons[:3]:
            lines.append(f"  • {reason}")
    lines.append("")
    
    # 识别实体
    entities = geo_data.get("entities", [])
    if entities:
        lines.append("**📍 关键实体识别**")
        for entity in entities[:5]:
            name = entity.get("name", "")
            category = entity.get("category", "")
            hotness = entity.get("hotness_score", 0)
            
            if hotness >= 80:
                lines.append(f"  🔥 <font color='red'>{name}</font> ({category}) - 热度: {hotness}")
            elif hotness >= 60:
                lines.append(f"  📈 <font color='orange'>{name}</font> ({category}) - 热度: {hotness}")
            else:
                lines.append(f"  📌 {name} ({category}) - 热度: {hotness}")
        lines.append("")
    
    # 转换桥梁 - 这是核心
    bridge = geo_data.get("conversation_bridge", {})
    if bridge:
        lines.append("**💡 营销话术转换（Hook-Bridge-CTA）**")
        hook = bridge.get("hook", "")
        bridge_text = bridge.get("bridge", "")
        cta = bridge.get("call_to_action", "")
        prob = bridge.get("conversion_probability", "")
        
        if hook:
            lines.append(f"<font color='green'>→ 勾子</font>: {hook}")
        if bridge_text:
            lines.append(f"<font color='blue'>→ 桥梁</font>: {bridge_text}")
        if cta:
            lines.append(f"<font color='red'>→ 行动召唤</font>: {cta}")
        if prob:
            lines.append(f"<font color='grey'>预估转化率: {prob}</font>")
        lines.append("")
    
    # 竞品分析
    competitor = geo_data.get("competitor_analysis", {})
    if competitor:
        target = competitor.get("target_brand", "")
        competitors = competitor.get("identified_competitors", [])
        insights = competitor.get("strategic_insights", [])
        
        lines.append(f"**🏆 竞品对标分析**")
        if target:
            lines.append(f"目标品牌: **{target}**")
        if competitors:
            lines.append(f"竞品: {', '.join(competitors[:5])}")
        if insights:
            lines.append("战略洞察:")
            for insight in insights[:3]:
                lines.append(f"  • {insight}")
        lines.append("")
    
    return "\n".join(lines)


def _render_geo_analysis_html(geo_data: dict) -> str:
    """渲染 GEO 分析为 HTML 格式"""
    html_parts = ['<div class="ai-analysis geo-analysis">', '<h3>🎯 GEO 营销机会分析</h3>']
    
    # 营销价值
    marketing_value = geo_data.get("marketing_value", {})
    score = marketing_value.get("score", 0)
    rating = marketing_value.get("overall_rating", "")
    reasons = marketing_value.get("reasons", [])
    
    rating_class_map = {
        "high_opportunity": "high",
        "medium_opportunity": "medium",
        "low_opportunity": "low",
        "not_suitable": "not-suitable"
    }
    rating_class = rating_class_map.get(rating, "")
    
    html_parts.append('<div class="ai-section geo-value">')
    html_parts.append('<h4>营销价值评估</h4>')
    html_parts.append(f'<div class="geo-score {rating_class}">评分: {score}/100</div>')
    if reasons:
        html_parts.append('<ul>')
        for reason in reasons[:3]:
            html_parts.append(f'<li>{_escape_html(reason)}</li>')
        html_parts.append('</ul>')
    html_parts.append('</div>')
    
    # 实体识别
    entities = geo_data.get("entities", [])
    if entities:
        html_parts.append('<div class="ai-section geo-entities">')
        html_parts.append('<h4>关键实体识别</h4>')
        html_parts.append('<ul>')
        for entity in entities[:5]:
            name = _escape_html(entity.get("name", ""))
            category = _escape_html(entity.get("category", ""))
            hotness = entity.get("hotness_score", 0)
            html_parts.append(f'<li><strong>{name}</strong> ({category}) - 热度: {hotness}</li>')
        html_parts.append('</ul>')
        html_parts.append('</div>')
    
    # 转换桥梁
    bridge = geo_data.get("conversation_bridge", {})
    if bridge:
        html_parts.append('<div class="ai-section geo-bridge">')
        html_parts.append('<h4>营销话术转换</h4>')
        
        hook = _escape_html(bridge.get("hook", ""))
        bridge_text = _escape_html(bridge.get("bridge", ""))
        cta = _escape_html(bridge.get("call_to_action", ""))
        
        if hook:
            html_parts.append(f'<div class="bridge-step"><strong>勾子:</strong> {hook}</div>')
        if bridge_text:
            html_parts.append(f'<div class="bridge-step"><strong>桥梁:</strong> {bridge_text}</div>')
        if cta:
            html_parts.append(f'<div class="bridge-step"><strong>行动召唤:</strong> {cta}</div>')
        html_parts.append('</div>')
    
    # 竞品分析
    competitor = geo_data.get("competitor_analysis", {})
    if competitor:
        html_parts.append('<div class="ai-section geo-competitor">')
        html_parts.append('<h4>竞品对标分析</h4>')
        
        target = _escape_html(competitor.get("target_brand", ""))
        competitors = competitor.get("identified_competitors", [])
        insights = competitor.get("strategic_insights", [])
        
        if target:
            html_parts.append(f'<p><strong>目标品牌:</strong> {target}</p>')
        if competitors:
            comps = ", ".join(_escape_html(c) for c in competitors[:5])
            html_parts.append(f'<p><strong>竞品:</strong> {comps}</p>')
        if insights:
            html_parts.append('<ul>')
            for insight in insights[:3]:
                html_parts.append(f'<li>{_escape_html(insight)}</li>')
            html_parts.append('</ul>')
        html_parts.append('</div>')
    
    html_parts.append('</div>')
    return "\n".join(html_parts)


def render_ai_analysis_markdown(result: AIAnalysisResult) -> str:
    """渲染为通用 Markdown 格式（Telegram、企业微信、ntfy、Bark、Slack）"""
    if not result.success:
        return f"⚠️ AI 分析失败: {result.error}"

    # GEO 模式
    if result.analysis_mode == "geo" and result.geo_data:
        return _render_geo_analysis_markdown(result.geo_data)

    # 通用模式
    lines = ["**✨ AI 热点分析**", ""]

    if result.core_trends:
        lines.extend(["**核心热点态势**", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["**舆论风向争议**", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["**异动与弱信号**", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["**RSS 深度洞察**", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["**研判策略建议**", _format_list_content(result.outlook_strategy)])

    return "\n".join(lines)


def render_ai_analysis_feishu(result: AIAnalysisResult) -> str:
    """渲染为飞书卡片 Markdown 格式"""
    if not result.success:
        return f"⚠️ AI 分析失败: {result.error}"

    # GEO 模式
    if result.analysis_mode == "geo" and result.geo_data:
        return _render_geo_analysis_feishu(result.geo_data)

    # 通用模式
    lines = ["**✨ AI 热点分析**", ""]

    if result.core_trends:
        lines.extend(["**核心热点态势**", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["**舆论风向争议**", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["**异动与弱信号**", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["**RSS 深度洞察**", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["**研判策略建议**", _format_list_content(result.outlook_strategy)])

    return "\n".join(lines)


def render_ai_analysis_dingtalk(result: AIAnalysisResult) -> str:
    """渲染为钉钉 Markdown 格式"""
    if not result.success:
        return f"⚠️ AI 分析失败: {result.error}"

    # GEO 模式 - 使用飞书格式（钉钉支持类似的 Markdown）
    if result.analysis_mode == "geo" and result.geo_data:
        return _render_geo_analysis_feishu(result.geo_data).replace("**✨", "### ✨").replace("**🎯", "### 🎯")

    # 通用模式
    lines = ["### ✨ AI 热点分析", ""]

    if result.core_trends:
        lines.extend(["#### 核心热点态势", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["#### 舆论风向争议", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["#### 异动与弱信号", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["#### RSS 深度洞察", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["#### 研判策略建议", _format_list_content(result.outlook_strategy)])

    return "\n".join(lines)


def render_ai_analysis_html(result: AIAnalysisResult) -> str:
    """渲染为 HTML 格式（邮件）"""
    if not result.success:
        return f'<div class="ai-error">⚠️ AI 分析失败: {_escape_html(result.error)}</div>'

    # GEO 模式
    if result.analysis_mode == "geo" and result.geo_data:
        return _render_geo_analysis_html(result.geo_data)

    # 通用模式
    html_parts = ['<div class="ai-analysis">', '<h3>✨ AI 热点分析</h3>']

    if result.core_trends:
        content = _format_list_content(result.core_trends)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend([
            '<div class="ai-section">',
            '<h4>核心热点态势</h4>',
            f'<div class="ai-content">{content_html}</div>',
            '</div>'
        ])

    if result.sentiment_controversy:
        content = _format_list_content(result.sentiment_controversy)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend([
            '<div class="ai-section">',
            '<h4>舆论风向争议</h4>',
            f'<div class="ai-content">{content_html}</div>',
            '</div>'
        ])

    if result.signals:
        content = _format_list_content(result.signals)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend([
            '<div class="ai-section">',
            '<h4>异动与弱信号</h4>',
            f'<div class="ai-content">{content_html}</div>',
            '</div>'
        ])

    if result.rss_insights:
        content = _format_list_content(result.rss_insights)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend([
            '<div class="ai-section">',
            '<h4>RSS 深度洞察</h4>',
            f'<div class="ai-content">{content_html}</div>',
            '</div>'
        ])

    if result.outlook_strategy:
        content = _format_list_content(result.outlook_strategy)
        content_html = _escape_html(content).replace("\n", "<br>")
        html_parts.extend([
            '<div class="ai-section ai-conclusion">',
            '<h4>研判策略建议</h4>',
            f'<div class="ai-content">{content_html}</div>',
            '</div>'
        ])

    html_parts.append('</div>')
    return "\n".join(html_parts)


def render_ai_analysis_plain(result: AIAnalysisResult) -> str:
    """渲染为纯文本格式"""
    if not result.success:
        return f"AI 分析失败: {result.error}"

    # GEO 模式 - 简化版
    if result.analysis_mode == "geo" and result.geo_data:
        return _render_geo_analysis_markdown(result.geo_data).replace("**", "").replace("<font color='", "[").replace("'></font>", "]")

    # 通用模式
    lines = ["【✨ AI 热点分析】", ""]

    if result.core_trends:
        lines.extend(["[核心热点态势]", _format_list_content(result.core_trends), ""])

    if result.sentiment_controversy:
        lines.extend(["[舆论风向争议]", _format_list_content(result.sentiment_controversy), ""])

    if result.signals:
        lines.extend(["[异动与弱信号]", _format_list_content(result.signals), ""])

    if result.rss_insights:
        lines.extend(["[RSS 深度洞察]", _format_list_content(result.rss_insights), ""])

    if result.outlook_strategy:
        lines.extend(["[研判策略建议]", _format_list_content(result.outlook_strategy)])

    return "\n".join(lines)


def get_ai_analysis_renderer(channel: str):
    """根据渠道获取对应的渲染函数"""
    renderers = {
        "feishu": render_ai_analysis_feishu,
        "dingtalk": render_ai_analysis_dingtalk,
        "wework": render_ai_analysis_markdown,
        "telegram": render_ai_analysis_markdown,
        "email": render_ai_analysis_html_rich,  # 邮件使用丰富样式，配合 HTML 报告的 CSS
        "ntfy": render_ai_analysis_markdown,
        "bark": render_ai_analysis_plain,
        "slack": render_ai_analysis_markdown,
    }
    return renderers.get(channel, render_ai_analysis_markdown)


def render_ai_analysis_html_rich(result: AIAnalysisResult) -> str:
    """渲染为丰富样式的 HTML 格式（HTML 报告用）"""
    if not result:
        return ""

    # 检查是否成功
    if not result.success:
        error_msg = result.error or "未知错误"
        return f'''
                <div class="ai-section">
                    <div class="ai-error">⚠️ AI 分析失败: {_escape_html(str(error_msg))}</div>
                </div>'''

    # GEO 模式
    if result.analysis_mode == "geo" and result.geo_data:
        return _render_geo_analysis_html(result.geo_data)

    # 通用模式
    ai_html = '''
                <div class="ai-section">
                    <div class="ai-section-header">
                        <div class="ai-section-title">✨ AI 热点分析</div>
                        <span class="ai-section-badge">AI</span>
                    </div>'''

    if result.core_trends:
        content = _format_list_content(result.core_trends)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">核心热点态势</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>'''

    if result.sentiment_controversy:
        content = _format_list_content(result.sentiment_controversy)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">舆论风向争议</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>'''

    if result.signals:
        content = _format_list_content(result.signals)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">异动与弱信号</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>'''

    if result.rss_insights:
        content = _format_list_content(result.rss_insights)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">RSS 深度洞察</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>'''

    if result.outlook_strategy:
        content = _format_list_content(result.outlook_strategy)
        content_html = _escape_html(content).replace("\n", "<br>")
        ai_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">研判策略建议</div>
                        <div class="ai-block-content">{content_html}</div>
                    </div>'''

    ai_html += '''
                </div>'''
    return ai_html
