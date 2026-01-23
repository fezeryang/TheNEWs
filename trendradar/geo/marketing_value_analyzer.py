# coding=utf-8
"""
营销价值判断模块

判断新闻是否具备"营销爆点"特质
评分体系（0-100分）并输出结构化的判定理由
"""

import json
from typing import Any, Dict, List, Optional

from trendradar.ai.client import AIClient
from trendradar.geo.prompt_templates import PromptTemplates


class MarketingValueAnalyzer:
    """营销价值分析器"""

    def __init__(self, ai_client: AIClient, language: str = "Chinese"):
        """
        初始化营销价值分析器

        Args:
            ai_client: AI 客户端实例
            language: 语言设置 (Chinese/English)
        """
        self.ai_client = ai_client
        self.language = language

    def analyze_marketing_value(
        self,
        title: str,
        content: str,
        entities: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        分析新闻的营销价值

        Args:
            title: 新闻标题
            content: 新闻内容
            entities: 已识别的实体列表（可选）

        Returns:
            Dict: 营销价值分析结果
            {
                "score": 88,
                "dimensions": {
                    "controversy": 75,
                    "new_product": 90,
                    "ranking_change": 60,
                    "topic_hotness": 85,
                    "timeliness": 95,
                    "industry_impact": 70
                },
                "reasons": ["新品发布", "社交热度高"],
                "marketing_angle": "创新升级",
                "target_audience": "科技爱好者",
                "success": True,
                "error": ""
            }
        """
        try:
            # 准备实体信息
            entities_str = ""
            if entities:
                # Use language-aware formatting
                separator = " (热度: " if self.language == "Chinese" else " (hotness: "
                entities_str = "\n".join(
                    [
                        f"- {e.get('name', '')} ({e.get('type', '')}){separator}{e.get('hotness_score', 0)})"
                        for e in entities[:5]  # 只传递前5个
                    ]
                )

            # 生成 Prompt
            prompt = PromptTemplates.format_prompt(
                task="marketing_value",
                language=self.language,
                title=title,
                content=content[:2000],  # 限制长度
                entities=entities_str or "无",
            )

            # 调用 AI
            messages = [
                {"role": "system", "content": "你是一个专业的营销价值分析专家。"},
                {"role": "user", "content": prompt},
            ]

            response = self.ai_client.chat(messages)

            # 解析 JSON 响应
            result = self._parse_json_response(response)

            if result and "score" in result:
                # 验证和规范化数据
                normalized = self._normalize_result(result)
                normalized["success"] = True
                normalized["error"] = ""
                return normalized
            else:
                return self._create_error_result("AI 返回格式错误")

        except Exception as e:
            return self._create_error_result(str(e))

    def analyze_batch(
        self, news_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量分析营销价值

        Args:
            news_list: 新闻列表，每条包含 title, content, entities

        Returns:
            List[Dict]: 每条新闻的营销价值分析结果
        """
        results = []
        for news in news_list:
            result = self.analyze_marketing_value(
                title=news.get("title", ""),
                content=news.get("content", ""),
                entities=news.get("entities", []),
            )
            result["news_id"] = news.get("id", "")
            result["news_title"] = news.get("title", "")
            results.append(result)
        return results

    def is_high_value(self, analysis_result: Dict[str, Any], threshold: int = 70) -> bool:
        """
        判断是否为高价值营销机会

        Args:
            analysis_result: 营销价值分析结果
            threshold: 分数阈值（默认70分）

        Returns:
            bool: 是否为高价值
        """
        return (
            analysis_result.get("success", False)
            and analysis_result.get("score", 0) >= threshold
        )

    def get_top_opportunities(
        self, results: List[Dict[str, Any]], top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        获取最佳营销机会（按分数排序）

        Args:
            results: 营销价值分析结果列表
            top_n: 返回前 N 个

        Returns:
            List[Dict]: 排序后的结果列表
        """
        # 过滤成功的结果
        valid_results = [r for r in results if r.get("success", False)]

        # 按分数降序排序
        sorted_results = sorted(
            valid_results, key=lambda x: x.get("score", 0), reverse=True
        )

        return sorted_results[:top_n]

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

    def _normalize_result(self, result: Dict) -> Dict[str, Any]:
        """规范化分析结果"""
        normalized = {
            "score": self._clamp_score(result.get("score", 0)),
            "dimensions": {},
            "reasons": result.get("reasons", []),
            "marketing_angle": result.get("marketing_angle", ""),
            "target_audience": result.get("target_audience", ""),
        }

        # 规范化各维度分数
        dimensions = result.get("dimensions", {})
        for dim in [
            "controversy",
            "new_product",
            "ranking_change",
            "topic_hotness",
            "timeliness",
            "industry_impact",
        ]:
            normalized["dimensions"][dim] = self._clamp_score(dimensions.get(dim, 0))

        return normalized

    def _clamp_score(self, score: Any) -> int:
        """限制分数在 0-100 范围内"""
        try:
            score_int = int(score)
            return max(0, min(100, score_int))
        except (ValueError, TypeError):
            return 0

    def _create_error_result(self, error: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "score": 0,
            "dimensions": {
                "controversy": 0,
                "new_product": 0,
                "ranking_change": 0,
                "topic_hotness": 0,
                "timeliness": 0,
                "industry_impact": 0,
            },
            "reasons": [],
            "marketing_angle": "",
            "target_audience": "",
            "success": False,
            "error": error,
        }
