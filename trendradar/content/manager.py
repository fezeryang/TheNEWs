# coding=utf-8
"""
内容管理器模块

负责将 AI 生成的内容保存到文件系统
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ContentManager:
    """内容管理器，负责保存生成的内容到文件"""

    def __init__(self, output_dir: str = "output/content"):
        """
        初始化内容管理器

        Args:
            output_dir: 内容输出目录
        """
        self.output_dir = Path(output_dir)

    def _sanitize_filename(self, filename: str, max_length: int = 50) -> str:
        """
        清理文件名，移除不安全字符

        Args:
            filename: 原始文件名
            max_length: 最大长度限制

        Returns:
            清理后的安全文件名
        """
        # 移除或替换不安全字符
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace('/', '-').replace('\\', '-')

        # 移除开头和结尾的空格和点
        filename = filename.strip(' .')

        # 限制长度
        if len(filename) > max_length:
            filename = filename[:max_length].strip()

        # 如果为空，使用默认名称
        if not filename:
            filename = "未命名内容"

        return filename

    def _create_date_folder(self, date_folder: str, subfolder: str) -> Path:
        """
        创建日期文件夹

        Args:
            date_folder: 日期文件夹名称（如 "2026-01-23"）
            subfolder: 子文件夹名称（xiaohongshu/wechat/prompts）

        Returns:
            创建的文件夹路径
        """
        folder = self.output_dir / subfolder / date_folder
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def save_xiaohongshu(
        self,
        content: Dict[str, Any],
        date_folder: str,
    ) -> Optional[str]:
        """
        保存小红书笔记到文件

        Args:
            content: AI 生成的小红书内容
            date_folder: 日期文件夹

        Returns:
            保存的文件路径，失败返回 None
        """
        if not content:
            return None

        try:
            from .renderer import render_xiaohongshu_for_save
            content_text = render_xiaohongshu_for_save(content)

            # 生成文件名
            title = content.get("title", "")
            safe_title = self._sanitize_filename(title)

            # 添加时间戳
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{timestamp}_{safe_title}.md"

            folder = self._create_date_folder(date_folder, "xiaohongshu")
            file_path = folder / filename

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content_text)

            return str(file_path)

        except Exception as e:
            print(f"[内容生产] 保存小红书内容失败: {e}")
            return None

    def save_wechat(
        self,
        content: Dict[str, Any],
        date_folder: str,
    ) -> Optional[str]:
        """
        保存公众号文章到文件

        Args:
            content: AI 生成的公众号文章
            date_folder: 日期文件夹

        Returns:
            保存的文件路径，失败返回 None
        """
        if not content:
            return None

        try:
            from .renderer import render_wechat_markdown
            content_text = render_wechat_markdown(content)

            # 生成文件名
            title = content.get("title", "")
            safe_title = self._sanitize_filename(title)

            # 添加时间戳
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{timestamp}_{safe_title}.md"

            folder = self._create_date_folder(date_folder, "wechat")
            file_path = folder / filename

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content_text)

            return str(file_path)

        except Exception as e:
            print(f"[内容生产] 保存公众号内容失败: {e}")
            return None

    def save_image_prompt(
        self,
        prompt: str,
        platform: str,
        topic: str,
        date_folder: str,
    ) -> Optional[str]:
        """
        保存图片提示词到文件

        Args:
            prompt: 图片提示词
            platform: 平台（xiaohongshu/wechat）
            topic: 主题词
            date_folder: 日期文件夹

        Returns:
            保存的文件路径，失败返回 None
        """
        if not prompt:
            return None

        try:
            # 生成文件名
            safe_topic = self._sanitize_filename(topic, max_length=30)
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{timestamp}_{platform}_{safe_topic}.txt"

            folder = self._create_date_folder(date_folder, "prompts")
            file_path = folder / filename

            content = f"# {platform.upper()} 配图提示词\n\n"
            content += f"# 主题: {topic}\n\n"
            content += f"# 提示词:\n{prompt}\n\n"
            content += f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return str(file_path)

        except Exception as e:
            print(f"[内容生产] 保存图片提示词失败: {e}")
            return None

    def save_all_content(
        self,
        ai_result: Any,
        date_folder: str,
    ) -> Dict[str, Optional[str]]:
        """
        保存所有生成的内容

        Args:
            ai_result: AI 分析结果
            date_folder: 日期文件夹

        Returns:
            各文件路径的字典
        """
        paths = {}

        if not ai_result or not ai_result.success:
            return paths

        # 保存小红书内容
        if ai_result.xiaohongshu_content:
            paths["xiaohongshu"] = self.save_xiaohongshu(
                ai_result.xiaohongshu_content,
                date_folder
            )

        # 保存公众号内容
        if ai_result.wechat_article:
            paths["wechat"] = self.save_wechat(
                ai_result.wechat_article,
                date_folder
            )

        # 保存小红书图片提示词
        if ai_result.xiaohongshu_content:
            prompt = ai_result.xiaohongshu_content.get("image_prompt", "")
            topic = ai_result.xiaohongshu_content.get("title", "未知主题")
            if prompt:
                paths["xiaohongshu_prompt"] = self.save_image_prompt(
                    prompt, "xiaohongshu", topic, date_folder
                )

        # 保存公众号图片提示词
        if ai_result.wechat_article:
            prompt = ai_result.wechat_article.get("image_prompt", "")
            topic = ai_result.wechat_article.get("title", "未知主题")
            if prompt:
                paths["wechat_prompt"] = self.save_image_prompt(
                    prompt, "wechat", topic, date_folder
                )

        return paths

    def get_content_summary(self, paths: Dict[str, Optional[str]]) -> str:
        """
        生成内容保存摘要

        Args:
            paths: 文件路径字典

        Returns:
            摘要信息字符串
        """
        if not paths:
            return ""

        lines = ["[内容生产] 内容已保存到：", ""]

        if paths.get("xiaohongshu"):
            lines.append(f"  📕 小红书: {paths['xiaohongongshu']}")
        if paths.get("wechat"):
            lines.append(f"  📊 公众号: {paths['wechat']}")
        if paths.get("xiaohongshu_prompt"):
            lines.append(f"  🎨 小红书配图: {paths['xiaohongshu_prompt']}")
        if paths.get("wechat_prompt"):
            lines.append(f"  🎨 公众号配图: {paths['wechat_prompt']}")

        return "\n".join(lines)
