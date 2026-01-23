# coding=utf-8
"""
竞品对比分析模块

基于识别出的品牌，自动收集竞品信息
生成品牌与竞品的对比分析框架
"""

import json
from typing import Any, Dict, List, Optional

from trendradar.ai.client import AIClient
from trendradar.geo.prompt_templates import PromptTemplates


class CompetitorAnalyzer:
    """竞品分析器"""

    def __init__(self, ai_client: AIClient, language: str = "Chinese"):
        """
        初始化竞品分析器

        Args:
            ai_client: AI 客户端实例
            language: 语言设置 (Chinese/English)
        """
        self.ai_client = ai_client
        self.language = language

    def analyze_competitors(
        self,
        brand: str,
        industry: Optional[str] = None,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        分析竞品

        Args:
            brand: 目标品牌
            industry: 行业背景（可选）
            context: 新闻上下文（可选）

        Returns:
            Dict: 竞品分析结果
            {
                "target_brand": "品牌名",
                "competitors": [
                    {
                        "name": "竞品名",
                        "reason": "选择原因",
                        "market_position": "市场定位"
                    }
                ],
                "comparison_dimensions": [
                    {
                        "dimension": "对比维度",
                        "description": "重要性说明",
                        "analysis_points": ["分析点1", "分析点2"]
                    }
                ],
                "geo_value": "GEO价值说明",
                "recommended_report_structure": ["章节1", "章节2"],
                "success": True,
                "error": ""
            }
        """
        try:
            # 生成 Prompt
            prompt = PromptTemplates.format_prompt(
                task="competitor_analysis",
                language=self.language,
                brand=brand,
                industry=industry or "未知",
                context=context[:1000] if context else "无",
            )

            # 调用 AI
            messages = [
                {"role": "system", "content": "你是一个专业的市场竞品分析专家。"},
                {"role": "user", "content": prompt},
            ]

            response = self.ai_client.chat(messages)

            # 解析 JSON 响应
            result = self._parse_json_response(response)

            if result and "target_brand" in result:
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
        批量分析竞品

        Args:
            news_list: 新闻列表，每条包含 brand, industry, context

        Returns:
            List[Dict]: 每条新闻的竞品分析结果
        """
        results = []
        for news in news_list:
            # 提取第一个品牌作为目标品牌
            brand = ""
            industry = ""
            if news.get("entities"):
                brands = [
                    e
                    for e in news["entities"]
                    if e.get("type") in ["brand", "company"]
                ]
                if brands:
                    brand = brands[0]["name"]

                industries = [
                    e for e in news["entities"] if e.get("type") == "industry"
                ]
                if industries:
                    industry = industries[0]["name"]

            if not brand:
                results.append(self._create_error_result("未找到品牌"))
                continue

            result = self.analyze_competitors(
                brand=brand,
                industry=industry,
                context=news.get("title", "") + "\n" + news.get("content", "")[:500],
            )
            result["news_id"] = news.get("id", "")
            result["news_title"] = news.get("title", "")
            results.append(result)

        return results

    def get_comparison_framework(
        self, analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        获取对比分析框架（用于 GEO 报告）

        Args:
            analysis_result: 竞品分析结果

        Returns:
            Dict: 简化的对比框架
        """
        if not analysis_result.get("success", False):
            return {}

        return {
            "target": analysis_result.get("target_brand", ""),
            "competitors": [
                c.get("name", "") for c in analysis_result.get("competitors", [])
            ],
            "dimensions": [
                d.get("dimension", "")
                for d in analysis_result.get("comparison_dimensions", [])
            ],
            "report_structure": analysis_result.get("recommended_report_structure", []),
        }

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
            "target_brand": result.get("target_brand", ""),
            "competitors": result.get("competitors", []),
            "comparison_dimensions": result.get("comparison_dimensions", []),
            "geo_value": result.get("geo_value", ""),
            "recommended_report_structure": result.get(
                "recommended_report_structure", []
            ),
        }

        # 确保竞品列表格式正确
        if normalized["competitors"]:
            for comp in normalized["competitors"]:
                if not isinstance(comp, dict):
                    continue
                comp.setdefault("name", "")
                comp.setdefault("reason", "")
                comp.setdefault("market_position", "")

        # 确保对比维度格式正确
        if normalized["comparison_dimensions"]:
            for dim in normalized["comparison_dimensions"]:
                if not isinstance(dim, dict):
                    continue
                dim.setdefault("dimension", "")
                dim.setdefault("description", "")
                dim.setdefault("analysis_points", [])

        return normalized

    def _create_error_result(self, error: str) -> Dict[str, Any]:
        """创建错误结果"""
        return {
            "target_brand": "",
            "competitors": [],
            "comparison_dimensions": [],
            "geo_value": "",
            "recommended_report_structure": [],
            "success": False,
            "error": error,
        }
