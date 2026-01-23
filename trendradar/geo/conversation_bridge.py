# coding=utf-8
"""
逻辑桥接模块

设计从"吃瓜/看新闻"到"需要做深度竞品分析报告"的话术转换路径
包含多套话术模板（技术对标、市场分析、用户决策等维度）
"""

import json
from typing import Any, Dict, List, Optional

from trendradar.ai.client import AIClient
from trendradar.geo.prompt_templates import PromptTemplates


class ConversationBridge:
    """话术桥接生成器"""

    def __init__(self, ai_client: AIClient, language: str = "Chinese"):
        """
        初始化话术桥接生成器

        Args:
            ai_client: AI 客户端实例
            language: 语言设置 (Chinese/English)
        """
        self.ai_client = ai_client
        self.language = language

    def generate_bridge(
        self,
        title: str,
        summary: str,
        brand: str,
        marketing_value: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        生成话术桥接

        Args:
            title: 新闻标题
            summary: 新闻摘要
            brand: 关键品牌
            marketing_value: 营销价值分析结果

        Returns:
            Dict: 话术桥接结果
            {
                "templates": [
                    {
                        "style": "技术对标",
                        "hook": "...",
                        "bridge": "...",
                        "call_to_action": "...",
                        "full_text": "..."
                    }
                ],
                "success": True,
                "error": ""
            }
        """
        try:
            # 准备营销价值摘要
            mv_summary = f"评分: {marketing_value.get('score', 0)}分"
            if marketing_value.get("reasons"):
                mv_summary += f", 原因: {', '.join(marketing_value['reasons'][:3])}"
            if marketing_value.get("marketing_angle"):
                mv_summary += f", 角度: {marketing_value['marketing_angle']}"

            # 生成 Prompt
            prompt = PromptTemplates.format_prompt(
                task="conversation_bridge",
                language=self.language,
                title=title,
                summary=summary[:500],  # 限制长度
                brand=brand,
                marketing_value=mv_summary,
            )

            # 调用 AI
            messages = [
                {"role": "system", "content": "你是一个专业的文案和营销话术专家。"},
                {"role": "user", "content": prompt},
            ]

            response = self.ai_client.chat(messages)

            # 解析 JSON 响应
            result = self._parse_json_response(response)

            if result and "templates" in result:
                # 验证模板格式
                templates = self._validate_templates(result["templates"])
                return {
                    "templates": templates,
                    "success": True,
                    "error": "",
                }
            else:
                return self._create_error_result("AI 返回格式错误")

        except Exception as e:
            return self._create_error_result(str(e))

    def generate_bridge_batch(
        self, news_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量生成话术桥接

        Args:
            news_list: 新闻列表，每条包含 title, summary, brand, marketing_value

        Returns:
            List[Dict]: 每条新闻的话术桥接结果
        """
        results = []
        for news in news_list:
            # 提取第一个品牌作为主品牌
            brand = ""
            if news.get("entities"):
                brands = [
                    e["name"]
                    for e in news["entities"]
                    if e.get("type") in ["brand", "company"]
                ]
                if brands:
                    brand = brands[0]

            if not brand:
                # 如果没有品牌，跳过
                results.append(self._create_error_result("未找到品牌"))
                continue

            result = self.generate_bridge(
                title=news.get("title", ""),
                summary=news.get("summary", news.get("content", "")[:200]),
                brand=brand,
                marketing_value=news.get("marketing_value", {}),
            )
            result["news_id"] = news.get("id", "")
            result["news_title"] = news.get("title", "")
            result["brand"] = brand
            results.append(result)

        return results

    def get_best_template(
        self, templates: List[Dict], style_preference: Optional[str] = None
    ) -> Optional[Dict]:
        """
        获取最佳话术模板

        Args:
            templates: 话术模板列表
            style_preference: 风格偏好（可选）

        Returns:
            Dict: 最佳模板，未找到返回 None
        """
        if not templates:
            return None

        # 如果指定了风格偏好
        if style_preference:
            for template in templates:
                if style_preference in template.get("style", ""):
                    return template

        # 否则返回第一个
        return templates[0]

    def _parse_json_response(self, response: str) -> Optional[Dict]:
        """解析 AI 返回的 JSON 响应"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            try:
                # 提取 JSON 部分
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                else:
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    if start != -1 and end > start:
                        json_str = response[start:end]
                    else:
                        return None
                return json.loads(json_str)
            except Exception:
                return None

    def _validate_templates(self, templates: List[Dict]) -> List[Dict]:
        """验证和规范化模板"""
        validated = []
        for template in templates:
            # 确保必需字段存在
            if not all(
                key in template
                for key in ["style", "hook", "bridge", "call_to_action"]
            ):
                continue

            # 规范化模板
            normalized = {
                "style": template.get("style", "未分类"),
                "hook": template.get("hook", ""),
                "bridge": template.get("bridge", ""),
                "call_to_action": template.get("call_to_action", ""),
                "full_text": template.get(
                    "full_text",
                    f"{template.get('hook', '')}\n\n{template.get('bridge', '')}\n\n{template.get('call_to_action', '')}",
                ),
            }
            validated.append(normalized)

        return validated

    def _create_error_result(self, error: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "templates": [],
            "success": False,
            "error": error,
        }
