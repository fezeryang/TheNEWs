# coding=utf-8
"""
实体识别模块

自动识别新闻中的品牌、产品、行业、人物等营销相关实体
基于 NLP 文本分析，不依赖预设关键词
"""

import json
from typing import Any, Dict, List, Optional

from trendradar.ai.client import AIClient
from trendradar.geo.prompt_templates import PromptTemplates


class EntityExtractor:
    """实体提取器"""

    def __init__(self, ai_client: AIClient, language: str = "Chinese"):
        """
        初始化实体提取器

        Args:
            ai_client: AI 客户端实例
            language: 语言设置 (Chinese/English)
        """
        self.ai_client = ai_client
        self.language = language

    def extract_entities(
        self, content: str, title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        从新闻内容中提取营销相关实体

        Args:
            content: 新闻内容
            title: 新闻标题（可选）

        Returns:
            Dict: 包含实体列表的字典
            {
                "entities": [
                    {
                        "name": "实体名称",
                        "type": "brand/product/person/industry/company",
                        "context": "上下文",
                        "hotness_score": 85,
                        "mentions": 3
                    }
                ],
                "success": True,
                "error": ""
            }
        """
        try:
            # 合并标题和内容
            full_content = content
            if title:
                full_content = f"标题：{title}\n\n内容：{content}"

            # 生成 Prompt
            prompt = PromptTemplates.format_prompt(
                task="entity_extraction",
                language=self.language,
                content=full_content[:3000],  # 限制长度避免 token 超限
            )

            # 调用 AI
            messages = [
                {"role": "system", "content": "你是一个专业的实体识别和分析专家。"},
                {"role": "user", "content": prompt},
            ]

            response = self.ai_client.chat(messages)

            # 解析 JSON 响应
            result = self._parse_json_response(response)

            if result and "entities" in result:
                # 过滤和排序实体
                entities = self._filter_and_sort_entities(result["entities"])
                return {
                    "entities": entities,
                    "success": True,
                    "error": "",
                }
            else:
                return {
                    "entities": [],
                    "success": False,
                    "error": "AI 返回格式错误",
                }

        except Exception as e:
            return {
                "entities": [],
                "success": False,
                "error": str(e),
            }

    def extract_entities_batch(
        self, news_list: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        批量提取实体

        Args:
            news_list: 新闻列表，每条包含 title 和 content

        Returns:
            List[Dict]: 每条新闻的实体提取结果
        """
        results = []
        for news in news_list:
            result = self.extract_entities(
                content=news.get("content", ""),
                title=news.get("title", ""),
            )
            result["news_id"] = news.get("id", "")
            result["news_title"] = news.get("title", "")
            results.append(result)
        return results

    def _parse_json_response(self, response: str) -> Optional[Dict]:
        """
        解析 AI 返回的 JSON 响应

        Args:
            response: AI 返回的字符串

        Returns:
            Dict: 解析后的字典，失败返回 None
        """
        try:
            # 尝试直接解析
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取 JSON 部分
            try:
                # 查找 JSON 代码块
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                else:
                    # 查找 { } 包裹的内容
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    if start != -1 and end > start:
                        json_str = response[start:end]
                    else:
                        return None

                return json.loads(json_str)
            except Exception:
                return None

    def _filter_and_sort_entities(self, entities: List[Dict]) -> List[Dict]:
        """
        过滤和排序实体

        Args:
            entities: 原始实体列表

        Returns:
            List[Dict]: 过滤和排序后的实体列表
        """
        # 过滤：移除热度分数过低的实体
        filtered = [e for e in entities if e.get("hotness_score", 0) >= 30]

        # 排序：按热度分数降序
        sorted_entities = sorted(
            filtered, key=lambda x: x.get("hotness_score", 0), reverse=True
        )

        # 限制数量（最多返回前 10 个）
        return sorted_entities[:10]

    def get_top_brands(
        self, entities: List[Dict], min_score: int = 50
    ) -> List[Dict]:
        """
        获取高热度品牌实体

        Args:
            entities: 实体列表
            min_score: 最低热度分数

        Returns:
            List[Dict]: 品牌实体列表
        """
        brands = [
            e
            for e in entities
            if e.get("type") in ["brand", "company"]
            and e.get("hotness_score", 0) >= min_score
        ]
        return brands

    def get_top_products(
        self, entities: List[Dict], min_score: int = 50
    ) -> List[Dict]:
        """
        获取高热度产品实体

        Args:
            entities: 实体列表
            min_score: 最低热度分数

        Returns:
            List[Dict]: 产品实体列表
        """
        products = [
            e
            for e in entities
            if e.get("type") == "product"
            and e.get("hotness_score", 0) >= min_score
        ]
        return products
