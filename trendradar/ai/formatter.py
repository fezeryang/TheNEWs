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


# ═══════════════════════════════════════════════════════════════
#                      GEO 分析结果格式化函数
# ═══════════════════════════════════════════════════════════════

def render_geo_analysis_markdown(result) -> str:
    """渲染 GEO 分析结果为 Markdown 格式"""
    from .geo_result import GEOAnalysisResult
    
    if not isinstance(result, GEOAnalysisResult):
        return ""
    
    if not result.success:
        return f"⚠️ GEO 分析失败: {result.error}"
    
    lines = ["**📊 GEO 借势分析**", ""]
    
    # 无实体情况
    if result.no_entity_reason:
        lines.append(f"ℹ️ {result.no_entity_reason}")
        return "\n".join(lines)
    
    # 识别的实体
    if result.entities:
        lines.append("**🎯 热点实体识别**")
        for i, entity in enumerate(result.entities, 1):
            lines.append(f"{i}. **{entity.name}** ({entity.type})")
            lines.append(f"   营销价值: {entity.marketing_value}/100")
            lines.append(f"   热度评分: {entity.hotness_score}/100")
            if entity.value_reasons:
                lines.append(f"   评分理由: {', '.join(entity.value_reasons)}")
        lines.append("")
    
    # 话术桥接
    if result.conversation_bridge:
        bridge = result.conversation_bridge
        lines.extend([
            "**💬 话术转换方案**",
            f"Hook: {bridge.hook}",
            f"Bridge: {bridge.bridge}",
            f"CTA: {bridge.cta}",
            ""
        ])
    
    # 竞品分析
    if result.competitor_analysis:
        comp = result.competitor_analysis
        lines.extend([
            "**🔍 竞品对比框架**",
            f"主品牌: {comp.brand}",
            f"竞品: {', '.join(comp.competitors)}",
            f"对比维度: {', '.join(comp.comparison_points)}",
            f"差异化点: {comp.differentiation}",
            ""
        ])
    
    # GEO 推荐
    if result.geo_recommendation:
        rec = result.geo_recommendation
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.priority, "⚪")
        lines.extend([
            "**✅ GEO 推荐**",
            f"推荐指数: {'推荐' if rec.recommended else '不推荐'}",
            f"优先级: {priority_emoji} {rec.priority.upper()}",
            f"信心度: {int(rec.confidence * 100)}%",
            f"执行计划: {rec.execution_plan}",
            f"预期效果: {rec.expected_outcome}",
        ])
    
    return "\n".join(lines)


def render_geo_analysis_feishu(result) -> str:
    """渲染 GEO 分析结果为飞书格式"""
    from .geo_result import GEOAnalysisResult
    
    if not isinstance(result, GEOAnalysisResult):
        return ""
    
    if not result.success:
        return f"⚠️ GEO 分析失败: {result.error}"
    
    lines = ["**📊 GEO 借势分析**", ""]
    
    # 无实体情况
    if result.no_entity_reason:
        lines.append(f"<font color='grey'>ℹ️ {result.no_entity_reason}</font>")
        return "\n".join(lines)
    
    # 识别的实体
    if result.entities:
        lines.append("**🎯 热点实体识别**\n")
        for i, entity in enumerate(result.entities, 1):
            lines.append(f"{i}. **{entity.name}** <font color='grey'>({entity.type})</font>")
            
            # 营销价值颜色
            value_color = "red" if entity.marketing_value >= 80 else ("orange" if entity.marketing_value >= 60 else "grey")
            lines.append(f"   营销价值: <font color='{value_color}'>{entity.marketing_value}/100</font>")
            lines.append(f"   热度评分: {entity.hotness_score}/100")
            
            if entity.value_reasons:
                lines.append(f"   评分理由: {', '.join(entity.value_reasons)}")
            lines.append("")
    
    # 话术桥接
    if result.conversation_bridge:
        bridge = result.conversation_bridge
        lines.extend([
            "**💬 话术转换方案**",
            f"Hook: {bridge.hook}",
            f"Bridge: {bridge.bridge}",
            f"CTA: <font color='blue'>{bridge.cta}</font>",
            ""
        ])
    
    # 竞品分析
    if result.competitor_analysis:
        comp = result.competitor_analysis
        lines.extend([
            "**🔍 竞品对比框架**",
            f"主品牌: **{comp.brand}**",
            f"竞品: {', '.join(comp.competitors)}",
            f"对比维度: {', '.join(comp.comparison_points)}",
            f"差异化点: {comp.differentiation}",
            ""
        ])
    
    # GEO 推荐
    if result.geo_recommendation:
        rec = result.geo_recommendation
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.priority, "⚪")
        rec_color = "green" if rec.recommended else "red"
        
        lines.extend([
            "**✅ GEO 推荐**",
            f"推荐指数: <font color='{rec_color}'>{'推荐' if rec.recommended else '不推荐'}</font>",
            f"优先级: {priority_emoji} **{rec.priority.upper()}**",
            f"信心度: {int(rec.confidence * 100)}%",
            f"执行计划: {rec.execution_plan}",
            f"预期效果: {rec.expected_outcome}",
        ])
    
    return "\n".join(lines)


def render_geo_analysis_html(result) -> str:
    """渲染 GEO 分析结果为 HTML 格式（用于 HTML 报告）"""
    from .geo_result import GEOAnalysisResult
    
    if not isinstance(result, GEOAnalysisResult):
        return ""
    
    if not result.success:
        return f'<div class="ai-error">⚠️ GEO 分析失败: {_escape_html(result.error)}</div>'
    
    geo_html = '''
                <div class="ai-analysis">
                    <div class="ai-title">📊 GEO 借势分析</div>'''
    
    # 无实体情况
    if result.no_entity_reason:
        geo_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-content">{_escape_html(result.no_entity_reason)}</div>
                    </div>
                </div>'''
        return geo_html
    
    # 识别的实体
    if result.entities:
        entities_content = ""
        for i, entity in enumerate(result.entities, 1):
            value_class = "high-value" if entity.marketing_value >= 80 else ("medium-value" if entity.marketing_value >= 60 else "low-value")
            entities_content += f'''
                <div class="entity-item">
                    <strong>{i}. {_escape_html(entity.name)}</strong> <span style="color: grey;">({_escape_html(entity.type)})</span><br>
                    营销价值: <span class="{value_class}">{entity.marketing_value}/100</span><br>
                    热度评分: {entity.hotness_score}/100<br>
            '''
            if entity.value_reasons:
                entities_content += f'评分理由: {_escape_html(", ".join(entity.value_reasons))}<br>'
            entities_content += '</div>'
        
        geo_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">🎯 热点实体识别</div>
                        <div class="ai-block-content">{entities_content}</div>
                    </div>'''
    
    # 话术桥接
    if result.conversation_bridge:
        bridge = result.conversation_bridge
        bridge_content = f'''
            <strong>Hook:</strong> {_escape_html(bridge.hook)}<br>
            <strong>Bridge:</strong> {_escape_html(bridge.bridge)}<br>
            <strong>CTA:</strong> {_escape_html(bridge.cta)}
        '''
        geo_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">💬 话术转换方案</div>
                        <div class="ai-block-content">{bridge_content}</div>
                    </div>'''
    
    # 竞品分析
    if result.competitor_analysis:
        comp = result.competitor_analysis
        comp_content = f'''
            <strong>主品牌:</strong> {_escape_html(comp.brand)}<br>
            <strong>竞品:</strong> {_escape_html(", ".join(comp.competitors))}<br>
            <strong>对比维度:</strong> {_escape_html(", ".join(comp.comparison_points))}<br>
            <strong>差异化点:</strong> {_escape_html(comp.differentiation)}
        '''
        geo_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">🔍 竞品对比框架</div>
                        <div class="ai-block-content">{comp_content}</div>
                    </div>'''
    
    # GEO 推荐
    if result.geo_recommendation:
        rec = result.geo_recommendation
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.priority, "⚪")
        rec_class = "recommended" if rec.recommended else "not-recommended"
        
        rec_content = f'''
            <strong>推荐指数:</strong> <span class="{rec_class}">{'推荐' if rec.recommended else '不推荐'}</span><br>
            <strong>优先级:</strong> {priority_emoji} <strong>{rec.priority.upper()}</strong><br>
            <strong>信心度:</strong> {int(rec.confidence * 100)}%<br>
            <strong>执行计划:</strong> {_escape_html(rec.execution_plan)}<br>
            <strong>预期效果:</strong> {_escape_html(rec.expected_outcome)}
        '''
        geo_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">✅ GEO 推荐</div>
                        <div class="ai-block-content">{rec_content}</div>
                    </div>'''
    
    geo_html += '''
                </div>'''
    return geo_html


def get_geo_analysis_renderer(channel: str):
    """根据渠道获取对应的 GEO 渲染函数"""
    renderers = {
        "feishu": render_geo_analysis_feishu,
        "dingtalk": render_geo_analysis_markdown,
        "wework": render_geo_analysis_markdown,
        "telegram": render_geo_analysis_markdown,
        "email": render_geo_analysis_html,
        "ntfy": render_geo_analysis_markdown,
        "bark": render_geo_analysis_markdown,
        "slack": render_geo_analysis_markdown,
    }
    return renderers.get(channel, render_geo_analysis_markdown)
