# coding=utf-8
"""
内容渲染模块

将 AI 生成的内容渲染为可直接发布或复制的格式
"""

from typing import Dict, Optional, Any


def render_xiaohongshu_for_copy(content: Dict[str, Any]) -> str:
    """渲染小红书内容为可直接复制发布的格式

    Args:
        content: AI 生成的小红书内容字典，包含 title, body, tags 等

    Returns:
        格式化后的小红书笔记内容，可直接复制到小红书发布
    """
    if not content:
        return ""

    lines = []

    # 标题
    title = content.get("title", "")
    if title:
        lines.append(f"{title}\n")

    # 正文
    body = content.get("body", "")
    if body:
        lines.append(f"{body}\n")

    # 标签
    tags = content.get("tags", [])
    if tags and isinstance(tags, list):
        tag_line = " ".join([f"#{tag}" for tag in tags[:5]])
        lines.append(tag_line)

    # 图片提示词（如果有）
    image_prompt = content.get("image_prompt", "")
    if image_prompt:
        lines.append(f"\n📸 配图提示词：\n{image_prompt}")

    # 封面建议（如果有）
    cover_idea = content.get("cover_idea", "")
    if cover_idea:
        lines.append(f"\n🎨 封面建议：{cover_idea}")

    return "\n".join(lines)


def render_xiaohongshu_for_save(content: Dict[str, Any]) -> str:
    """渲染小红书内容为保存到文件的格式（包含元信息）

    Args:
        content: AI 生成的小红书内容字典

    Returns:
        包含元信息的 Markdown 格式内容
    """
    if not content:
        return ""

    lines = ["# 小红书笔记\n"]

    # 标题
    title = content.get("title", "")
    if title:
        lines.append(f"**标题**: {title}\n")

    # 正文
    body = content.get("body", "")
    if body:
        lines.append(f"**正文**:\n{body}\n")

    # 标签
    tags = content.get("tags", [])
    if tags and isinstance(tags, list):
        tags_str = " | ".join([f"#{tag}" for tag in tags[:5]])
        lines.append(f"**标签**: {tags_str}\n")

    # 图片提示词
    image_prompt = content.get("image_prompt", "")
    if image_prompt:
        lines.append(f"**配图提示词**:\n```\n{image_prompt}\n```\n")

    # 封面建议
    cover_idea = content.get("cover_idea", "")
    if cover_idea:
        lines.append(f"**封面建议**: {cover_idea}\n")

    # 发布时间戳
    from datetime import datetime
    lines.append(f"\n---\n\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(lines)


def render_wechat_markdown(content: Dict[str, Any]) -> str:
    """渲染公众号文章为 Markdown 格式

    Args:
        content: AI 生成的公众号文章字典

    Returns:
        Markdown 格式的文章内容
    """
    if not content:
        return ""

    lines = []

    # 标题
    title = content.get("title", "")
    if title:
        lines.append(f"# {title}\n")

    # 摘要
    summary = content.get("summary", "")
    if summary:
        lines.append(f"> {summary}\n")

    # 正文
    body = content.get("body", "")
    if body:
        lines.append(f"{body}\n")

    # 图片提示词
    image_prompt = content.get("image_prompt", "")
    if image_prompt:
        lines.append(f"---\n## 封面图\n\n**AI 配图提示词**:\n```\n{image_prompt}\n```\n")

    # 封面建议
    cover_idea = content.get("cover_idea", "")
    if cover_idea:
        lines.append(f"**设计建议**: {cover_idea}\n")

    # 发布时间
    from datetime import datetime
    lines.append(f"\n---\n\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(lines)


def render_wechat_html(content: Dict[str, Any]) -> str:
    """渲染公众号文章为 HTML 格式（适合公众号编辑器）

    Args:
        content: AI 生成的公众号文章字典

    Returns:
        HTML 格式的文章内容
    """
    if not content:
        return ""

    # 转换 Markdown 到 HTML（简化版）
    md_content = render_wechat_markdown(content)

    # 简单的 Markdown 到 HTML 转换
    import re

    # 标题
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md_content, flags=re.MULTILINE)

    # 二级标题
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)

    # 三级标题
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)

    # 四级标题
    html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)

    # 引用块
    html_content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)

    # 粗体（如果正文中有 **text** 格式）
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

    # 换行
    html_content = html_content.replace("\n\n", "</p><p>")
    html_content = f"<p>{html_content}</p>"

    # 代码块
    html_content = re.sub(r'<p>```</p>', '<pre>', html_content)
    html_content = re.sub(r'<p>(.+?)</p>', r'</pre><p>\1</p>', html_content, flags=re.DOTALL)

    # 时间戳
    html_content = re.sub(r'\*生成时间: .+\*', '<em><small>\g<0></em></small>', html_content)

    return html_content


def render_content_preview(
    ai_result: Any,
    max_length: int = 200,
    show_platforms: list[str] = ["xiaohongshu", "wechat"],
) -> str:
    """渲染内容预览，用于通知消息中展示

    Args:
        ai_result: AI 分析结果
        max_length: 预览最大长度
        show_platforms: 要预览的平台列表

    Returns:
        预览内容字符串
    """
    if not ai_result or not ai_result.success:
        return ""

    lines = ["📝 **内容生成预览**", ""]
    has_content = False

    if "xiaohongshu" in show_platforms and ai_result.xiaohongshu_content:
        has_content = True
        title = ai_result.xiaohongshu_content.get("title", "")[:30]
        body = ai_result.xiaohongshu_content.get("body", "")[:80]
        lines.append(f"📕 小红书: {title}")
        lines.append(f"   {body}...")

    if "wechat" in show_platforms and ai_result.wechat_article:
        if has_content:
            lines.append("")
        has_content = True
        title = ai_result.wechat_article.get("title", "")[:30]
        summary = ai_result.wechat_article.get("summary", "")[:50]
        lines.append(f"📊 公众号: {title}")
        lines.append(f"   {summary}...")

    if not has_content:
        return ""

    preview = "\n".join(lines)

    if len(preview) > max_length:
        preview = preview[:max_length] + "..."

    return preview


def render_content_list(ai_result: Any) -> str:
    """渲染内容列表，用于显示已生成的内容文件

    Args:
        ai_result: AI 分析结果

    Returns:
        内容列表字符串
    """
    if not ai_result or not ai_result.success:
        return "无内容生成"

    items = []

    if ai_result.xiaohongshu_content:
        title = ai_result.xiaohongshu_content.get("title", "")
        items.append(f"• 📕 小红书: {title}")

    if ai_result.wechat_article:
        title = ai_result.wechat_article.get("title", "")
        items.append(f"• 📊 公众号: {title}")

    if items:
        return "\n".join(items)
    else:
        return "无内容生成"
