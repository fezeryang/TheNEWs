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


def render_ai_analysis_markdown(result: AIAnalysisResult) -> str:
    """渲染为通用 Markdown 格式（Telegram、企业微信、ntfy、Bark、Slack）"""
    if result.is_geo_mode:
        return render_geo_analysis_markdown(result)
    
    if not result.success:
        return f"⚠️ AI 分析失败: {result.error}"

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
    if result.is_geo_mode:
        return render_geo_analysis_feishu(result)
    
    if not result.success:
        return f"⚠️ AI 分析失败: {result.error}"

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
    if result.is_geo_mode:
        return render_geo_analysis_dingtalk(result)
    
    if not result.success:
        return f"⚠️ AI 分析失败: {result.error}"

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


# ============================================================================
# GEO 营销分析渲染函数
# ============================================================================

def render_geo_analysis_markdown(result: AIAnalysisResult) -> str:
    """渲染 GEO 营销分析为 Markdown 格式（通用）"""
    if not result.success:
        return f"⚠️ GEO 营销分析失败: {result.error}"
    
    if not result.is_geo_mode:
        return "⚠️ 非 GEO 模式分析结果"
    
    lines = ["**🎯 GEO 营销机会分析**", ""]
    
    # 1. 实体识别
    if result.geo_entities:
        lines.append("**🏷️ 识别品牌/产品**")
        for entity in result.geo_entities:
            name = entity.get("name", "")
            etype = entity.get("type", "")
            category = entity.get("category", "")
            hotness = entity.get("hotness_score", 0)
            impact = entity.get("market_impact", "")
            lines.append(f"• {name} ({etype}) - {category} | 热度:{hotness} | 影响:{impact}")
        lines.append("")
    
    # 2. 营销价值评估
    if result.geo_marketing_value:
        mv = result.geo_marketing_value
        score = mv.get("score", 0)
        rating = mv.get("overall_rating", "")
        lines.append(f"**📊 营销价值评分: {score}/100** ({rating})")
        
        dimensions = mv.get("dimensions", {})
        if dimensions:
            lines.append("维度得分:")
            lines.append(f"  争议性:{dimensions.get('controversy',0)} | 新品:{dimensions.get('new_product',0)} | 排名变化:{dimensions.get('ranking_change',0)}")
            lines.append(f"  话题热度:{dimensions.get('topic_heat',0)} | 时效性:{dimensions.get('timeliness',0)} | 行业影响:{dimensions.get('industry_impact',0)}")
        
        reasons = mv.get("reasons", [])
        if reasons:
            lines.append("价值点:")
            for reason in reasons:
                lines.append(f"  • {reason}")
        lines.append("")
    
    # 3. 转化漏斗设计
    if result.geo_conversation_bridge:
        cb = result.geo_conversation_bridge
        lines.append("**🎣 转化漏斗设计**")
        lines.append(f"Hook: {cb.get('hook', '')}")
        lines.append(f"Bridge: {cb.get('bridge', '')}")
        lines.append(f"CTA: {cb.get('call_to_action', '')}")
        lines.append("")
    
    # 4. 竞品分析
    if result.geo_competitor_analysis:
        ca = result.geo_competitor_analysis
        target = ca.get("target_brand", "")
        competitors = ca.get("identified_competitors", [])
        if target and competitors:
            lines.append(f"**🔍 竞品对比: {target}**")
            lines.append(f"主要竞争对手: {', '.join(competitors)}")
            
            dimensions = ca.get("comparison_dimensions", [])
            if dimensions:
                lines.append(f"对比维度: {', '.join(dimensions)}")
            
            insights = ca.get("strategic_insights", [])
            if insights:
                lines.append("战略洞察:")
                for insight in insights:
                    lines.append(f"  • {insight}")
            lines.append("")
    
    # 5. 执行建议
    if result.geo_recommendation:
        rec = result.geo_recommendation
        recommended = rec.get("recommended", False)
        priority = rec.get("priority", "")
        confidence = rec.get("confidence", 0)
        
        status_icon = "✅" if recommended else "❌"
        lines.append(f"**{status_icon} 推荐度: {'推荐' if recommended else '不推荐'}** | 优先级:{priority} | 置信度:{confidence:.0%}")
        
        if recommended:
            exec_plan = rec.get("execution_plan", {})
            if exec_plan:
                lines.append("执行计划:")
                lines.append(f"  1️⃣ {exec_plan.get('phase_1_traffic', '')}")
                lines.append(f"  2️⃣ {exec_plan.get('phase_2_engagement', '')}")
                lines.append(f"  3️⃣ {exec_plan.get('phase_3_conversion', '')}")
                lines.append(f"  📈 预估转化率: {exec_plan.get('estimated_conversion_rate', '')}")
            
            risk = rec.get("risk_assessment", "")
            leads = rec.get("expected_leads", "")
            if risk:
                lines.append(f"风险评估: {risk}")
            if leads:
                lines.append(f"预期线索: {leads}")
    
    return "\n".join(lines)


def render_geo_analysis_feishu(result: AIAnalysisResult) -> str:
    """渲染 GEO 营销分析为飞书格式"""
    if not result.success:
        return f"⚠️ GEO 营销分析失败: {result.error}"
    
    if not result.is_geo_mode:
        return "⚠️ 非 GEO 模式分析结果"
    
    lines = ["**🎯 GEO 营销机会分析**", ""]
    
    # 1. 实体识别
    if result.geo_entities:
        lines.append("**🏷️ 识别品牌/产品**")
        for entity in result.geo_entities:
            name = entity.get("name", "")
            etype = entity.get("type", "")
            category = entity.get("category", "")
            hotness = entity.get("hotness_score", 0)
            impact = entity.get("market_impact", "")
            lines.append(f"• {name} <font color='grey'>({etype})</font> - {category} | <font color='orange'>热度:{hotness}</font> | 影响:{impact}")
        lines.append("")
    
    # 2. 营销价值评估
    if result.geo_marketing_value:
        mv = result.geo_marketing_value
        score = mv.get("score", 0)
        rating = mv.get("overall_rating", "")
        
        score_color = "red" if score >= 80 else "orange" if score >= 60 else "grey"
        lines.append(f"**📊 营销价值评分: <font color='{score_color}'>{score}/100</font>** ({rating})")
        
        dimensions = mv.get("dimensions", {})
        if dimensions:
            lines.append("维度得分:")
            lines.append(f"  争议性:{dimensions.get('controversy',0)} | 新品:{dimensions.get('new_product',0)} | 排名变化:{dimensions.get('ranking_change',0)}")
            lines.append(f"  话题热度:{dimensions.get('topic_heat',0)} | 时效性:{dimensions.get('timeliness',0)} | 行业影响:{dimensions.get('industry_impact',0)}")
        
        reasons = mv.get("reasons", [])
        if reasons:
            lines.append("价值点:")
            for reason in reasons:
                lines.append(f"  • {reason}")
        lines.append("")
    
    # 3. 转化漏斗设计
    if result.geo_conversation_bridge:
        cb = result.geo_conversation_bridge
        lines.append("**🎣 转化漏斗设计**")
        lines.append(f"<font color='blue'>Hook:</font> {cb.get('hook', '')}")
        lines.append(f"<font color='blue'>Bridge:</font> {cb.get('bridge', '')}")
        lines.append(f"<font color='blue'>CTA:</font> {cb.get('call_to_action', '')}")
        lines.append("")
    
    # 4. 竞品分析
    if result.geo_competitor_analysis:
        ca = result.geo_competitor_analysis
        target = ca.get("target_brand", "")
        competitors = ca.get("identified_competitors", [])
        if target and competitors:
            lines.append(f"**🔍 竞品对比: {target}**")
            lines.append(f"主要竞争对手: {', '.join(competitors)}")
            
            dimensions = ca.get("comparison_dimensions", [])
            if dimensions:
                lines.append(f"对比维度: {', '.join(dimensions)}")
            
            insights = ca.get("strategic_insights", [])
            if insights:
                lines.append("战略洞察:")
                for insight in insights:
                    lines.append(f"  • {insight}")
            lines.append("")
    
    # 5. 执行建议
    if result.geo_recommendation:
        rec = result.geo_recommendation
        recommended = rec.get("recommended", False)
        priority = rec.get("priority", "")
        confidence = rec.get("confidence", 0)
        
        status_icon = "✅" if recommended else "❌"
        status_color = "green" if recommended else "grey"
        lines.append(f"**{status_icon} 推荐度: <font color='{status_color}'>{'推荐' if recommended else '不推荐'}</font>** | 优先级:{priority} | 置信度:{confidence:.0%}")
        
        if recommended:
            exec_plan = rec.get("execution_plan", {})
            if exec_plan:
                lines.append("执行计划:")
                lines.append(f"  1️⃣ {exec_plan.get('phase_1_traffic', '')}")
                lines.append(f"  2️⃣ {exec_plan.get('phase_2_engagement', '')}")
                lines.append(f"  3️⃣ {exec_plan.get('phase_3_conversion', '')}")
                lines.append(f"  📈 预估转化率: {exec_plan.get('estimated_conversion_rate', '')}")
            
            risk = rec.get("risk_assessment", "")
            leads = rec.get("expected_leads", "")
            if risk:
                lines.append(f"<font color='grey'>风险评估: {risk}</font>")
            if leads:
                lines.append(f"<font color='grey'>预期线索: {leads}</font>")
    
    return "\n".join(lines)


def render_geo_analysis_dingtalk(result: AIAnalysisResult) -> str:
    """渲染 GEO 营销分析为钉钉格式"""
    if not result.success:
        return f"⚠️ GEO 营销分析失败: {result.error}"
    
    if not result.is_geo_mode:
        return "⚠️ 非 GEO 模式分析结果"
    
    lines = ["### 🎯 GEO 营销机会分析", ""]
    
    # 1. 实体识别
    if result.geo_entities:
        lines.append("#### 🏷️ 识别品牌/产品")
        for entity in result.geo_entities:
            name = entity.get("name", "")
            etype = entity.get("type", "")
            category = entity.get("category", "")
            hotness = entity.get("hotness_score", 0)
            impact = entity.get("market_impact", "")
            lines.append(f"• **{name}** ({etype}) - {category} | 热度:**{hotness}** | 影响:{impact}")
        lines.append("")
    
    # 2. 营销价值评估
    if result.geo_marketing_value:
        mv = result.geo_marketing_value
        score = mv.get("score", 0)
        rating = mv.get("overall_rating", "")
        lines.append(f"#### 📊 营销价值评分: **{score}/100** ({rating})")
        
        dimensions = mv.get("dimensions", {})
        if dimensions:
            lines.append("维度得分:")
            lines.append(f"  争议性:{dimensions.get('controversy',0)} | 新品:{dimensions.get('new_product',0)} | 排名变化:{dimensions.get('ranking_change',0)}")
            lines.append(f"  话题热度:{dimensions.get('topic_heat',0)} | 时效性:{dimensions.get('timeliness',0)} | 行业影响:{dimensions.get('industry_impact',0)}")
        
        reasons = mv.get("reasons", [])
        if reasons:
            lines.append("价值点:")
            for reason in reasons:
                lines.append(f"  • {reason}")
        lines.append("")
    
    # 3. 转化漏斗设计
    if result.geo_conversation_bridge:
        cb = result.geo_conversation_bridge
        lines.append("#### 🎣 转化漏斗设计")
        lines.append(f"**Hook:** {cb.get('hook', '')}")
        lines.append(f"**Bridge:** {cb.get('bridge', '')}")
        lines.append(f"**CTA:** {cb.get('call_to_action', '')}")
        lines.append("")
    
    # 4. 竞品分析
    if result.geo_competitor_analysis:
        ca = result.geo_competitor_analysis
        target = ca.get("target_brand", "")
        competitors = ca.get("identified_competitors", [])
        if target and competitors:
            lines.append(f"#### 🔍 竞品对比: {target}")
            lines.append(f"主要竞争对手: {', '.join(competitors)}")
            
            dimensions = ca.get("comparison_dimensions", [])
            if dimensions:
                lines.append(f"对比维度: {', '.join(dimensions)}")
            
            insights = ca.get("strategic_insights", [])
            if insights:
                lines.append("战略洞察:")
                for insight in insights:
                    lines.append(f"  • {insight}")
            lines.append("")
    
    # 5. 执行建议
    if result.geo_recommendation:
        rec = result.geo_recommendation
        recommended = rec.get("recommended", False)
        priority = rec.get("priority", "")
        confidence = rec.get("confidence", 0)
        
        status_icon = "✅" if recommended else "❌"
        lines.append(f"#### {status_icon} 推荐度: **{'推荐' if recommended else '不推荐'}** | 优先级:{priority} | 置信度:{confidence:.0%}")
        
        if recommended:
            exec_plan = rec.get("execution_plan", {})
            if exec_plan:
                lines.append("执行计划:")
                lines.append(f"  1️⃣ {exec_plan.get('phase_1_traffic', '')}")
                lines.append(f"  2️⃣ {exec_plan.get('phase_2_engagement', '')}")
                lines.append(f"  3️⃣ {exec_plan.get('phase_3_conversion', '')}")
                lines.append(f"  📈 预估转化率: {exec_plan.get('estimated_conversion_rate', '')}")
            
            risk = rec.get("risk_assessment", "")
            leads = rec.get("expected_leads", "")
            if risk:
                lines.append(f"> 风险评估: {risk}")
            if leads:
                lines.append(f"> 预期线索: {leads}")
    
    return "\n".join(lines)
