# coding=utf-8
"""
GEO 推荐引擎

综合所有分析模块，生成完整的 GEO 推荐方案
输出格式：JSON / 结构化数据
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from trendradar.ai.client import AIClient
from trendradar.geo.entity_extractor import EntityExtractor
from trendradar.geo.marketing_value_analyzer import MarketingValueAnalyzer
from trendradar.geo.conversation_bridge import ConversationBridge
from trendradar.geo.competitor_analysis import CompetitorAnalyzer
from trendradar.geo.prompt_templates import PromptTemplates


class GEORecommendationEngine:
    """GEO 推荐引擎"""

    def __init__(
        self,
        ai_client: AIClient,
        language: str = "Chinese",
        output_dir: str = "output/geo_analysis",
    ):
        """
        初始化 GEO 推荐引擎

        Args:
            ai_client: AI 客户端实例
            language: 语言设置 (Chinese/English)
            output_dir: 输出目录
        """
        self.ai_client = ai_client
        self.language = language
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 初始化各模块
        self.entity_extractor = EntityExtractor(ai_client, language)
        self.marketing_analyzer = MarketingValueAnalyzer(ai_client, language)
        self.conversation_bridge = ConversationBridge(ai_client, language)
        self.competitor_analyzer = CompetitorAnalyzer(ai_client, language)

    def analyze_news(self, news: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析单条新闻，生成完整的 GEO 推荐

        Args:
            news: 新闻数据，包含 id, title, content, url 等

        Returns:
            Dict: 完整的 GEO 推荐结果
        """
        news_id = news.get("id", "unknown")
        title = news.get("title", "")
        content = news.get("content", "")
        url = news.get("url", "")

        print(f"[GEO] 正在分析新闻: {title}")

        result = {
            "news_id": news_id,
            "title": title,
            "url": url,
            "analyzed_at": datetime.now().isoformat(),
        }

        # 1. 实体识别
        print(f"[GEO]   - 步骤 1/5: 实体识别")
        entity_result = self.entity_extractor.extract_entities(content, title)
        result["entities"] = entity_result.get("entities", [])

        if not result["entities"]:
            print(f"[GEO]   ✗ 未识别到实体，跳过该新闻")
            result["recommended"] = False
            result["skip_reason"] = "未识别到营销相关实体"
            return result

        # 2. 营销价值分析
        print(f"[GEO]   - 步骤 2/5: 营销价值分析")
        marketing_result = self.marketing_analyzer.analyze_marketing_value(
            title, content, result["entities"]
        )
        result["marketing_value"] = marketing_result

        # 判断是否值得继续分析（营销分数 >= 60）
        if marketing_result.get("score", 0) < 60:
            print(
                f"[GEO]   ✗ 营销价值过低 ({marketing_result.get('score', 0)}分)，跳过"
            )
            result["recommended"] = False
            result["skip_reason"] = "营销价值评分过低"
            return result

        # 提取主品牌
        brands = self.entity_extractor.get_top_brands(result["entities"])
        if not brands:
            print(f"[GEO]   ✗ 未识别到品牌实体，跳过")
            result["recommended"] = False
            result["skip_reason"] = "未识别到品牌实体"
            return result

        main_brand = brands[0]["name"]
        result["main_brand"] = main_brand

        # 3. 话术桥接生成
        print(f"[GEO]   - 步骤 3/5: 话术桥接生成")
        bridge_result = self.conversation_bridge.generate_bridge(
            title=title,
            summary=content[:200],
            brand=main_brand,
            marketing_value=marketing_result,
        )
        result["conversation_bridge"] = bridge_result

        # 4. 竞品分析
        print(f"[GEO]   - 步骤 4/5: 竞品分析")
        # 提取行业信息
        industry = ""
        industries = [e for e in result["entities"] if e.get("type") == "industry"]
        if industries:
            industry = industries[0]["name"]

        competitor_result = self.competitor_analyzer.analyze_competitors(
            brand=main_brand,
            industry=industry,
            context=title + "\n" + content[:500],
        )
        result["competitor_analysis"] = competitor_result

        # 5. 生成 GEO 推荐
        print(f"[GEO]   - 步骤 5/5: 生成 GEO 推荐")
        geo_recommendation = self._generate_geo_recommendation(result)
        result["geo_recommendation"] = geo_recommendation

        print(
            f"[GEO]   ✓ 分析完成 (推荐: {geo_recommendation.get('recommended', False)}, "
            f"优先级: {geo_recommendation.get('priority', 'N/A')})"
        )

        return result

    def analyze_news_batch(
        self, news_list: List[Dict[str, Any]], max_news: int = 10
    ) -> List[Dict[str, Any]]:
        """
        批量分析新闻

        Args:
            news_list: 新闻列表
            max_news: 最多分析的新闻数量

        Returns:
            List[Dict]: GEO 推荐结果列表
        """
        print(f"[GEO] 开始批量分析 {min(len(news_list), max_news)} 条新闻")
        results = []

        for i, news in enumerate(news_list[:max_news]):
            print(f"[GEO] 进度: {i+1}/{min(len(news_list), max_news)}")
            try:
                result = self.analyze_news(news)
                results.append(result)
            except Exception as e:
                print(f"[GEO] 分析失败: {e}")
                results.append(
                    {
                        "news_id": news.get("id", "unknown"),
                        "title": news.get("title", ""),
                        "error": str(e),
                        "recommended": False,
                    }
                )

        print(f"[GEO] 批量分析完成，共 {len(results)} 条结果")
        return results

    def save_results(
        self, results: List[Dict[str, Any]], filename: Optional[str] = None
    ) -> str:
        """
        保存分析结果到文件

        Args:
            results: 分析结果列表
            filename: 文件名（可选，默认使用时间戳）

        Returns:
            str: 保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"geo_analysis_{timestamp}.json"

        filepath = self.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"[GEO] 结果已保存到: {filepath}")
        return str(filepath)

    def get_high_priority_recommendations(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        获取高优先级推荐

        Args:
            results: 分析结果列表

        Returns:
            List[Dict]: 高优先级推荐列表
        """
        high_priority = [
            r
            for r in results
            if r.get("geo_recommendation", {}).get("recommended", False)
            and r.get("geo_recommendation", {}).get("priority") == "high"
        ]
        return sorted(
            high_priority,
            key=lambda x: x.get("geo_recommendation", {}).get("confidence_score", 0),
            reverse=True,
        )

    def _generate_geo_recommendation(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成 GEO 推荐（基于前面的分析结果）

        Args:
            analysis_result: 包含所有分析结果的字典

        Returns:
            Dict: GEO 推荐
        """
        try:
            # 准备输入数据
            news_info = f"标题: {analysis_result.get('title', '')}"

            entities_summary = ", ".join(
                [e.get("name", "") for e in analysis_result.get("entities", [])[:3]]
            )

            marketing_value = analysis_result.get("marketing_value", {})
            mv_summary = f"评分: {marketing_value.get('score', 0)}, 角度: {marketing_value.get('marketing_angle', '')}"

            conv_bridge = analysis_result.get("conversation_bridge", {})
            cb_summary = "已生成" if conv_bridge.get("success") else "未生成"

            comp_analysis = analysis_result.get("competitor_analysis", {})
            ca_summary = (
                f"目标: {comp_analysis.get('target_brand', '')}, "
                f"竞品数: {len(comp_analysis.get('competitors', []))}"
            )

            # 生成 Prompt
            prompt = PromptTemplates.format_prompt(
                task="geo_recommendation",
                language=self.language,
                news_info=news_info,
                entities=entities_summary,
                marketing_value=mv_summary,
                conversation_bridge=cb_summary,
                competitor_analysis=ca_summary,
            )

            # 调用 AI
            messages = [
                {"role": "system", "content": "你是一个专业的 GEO 营销策略专家。"},
                {"role": "user", "content": prompt},
            ]

            response = self.ai_client.chat(messages)

            # 解析 JSON 响应
            result = self._parse_json_response(response)

            if result and "recommended" in result:
                # 确保必需字段存在
                result.setdefault("confidence_score", 70)
                result.setdefault("priority", "medium")
                result.setdefault("execution_plan", {})
                result.setdefault("expected_results", {})
                result.setdefault("content_angles", [])
                result.setdefault("risks", [])
                result.setdefault("next_steps", [])
                return result
            else:
                # 使用默认推荐逻辑
                return self._create_default_recommendation(analysis_result)

        except Exception as e:
            print(f"[GEO] 生成推荐失败: {e}")
            return self._create_default_recommendation(analysis_result)

    def _create_default_recommendation(
        self, analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """创建默认推荐（当 AI 调用失败时）"""
        marketing_score = analysis_result.get("marketing_value", {}).get("score", 0)

        return {
            "recommended": marketing_score >= 70,
            "confidence_score": marketing_score,
            "priority": "high" if marketing_score >= 80 else "medium",
            "execution_plan": {
                "content_strategy": "基于新闻热度制作 GEO 内容",
                "channels": ["社交媒体", "博客", "行业论坛"],
                "timing": "24小时内",
                "key_messages": ["品牌对比", "竞品分析", "决策建议"],
            },
            "expected_results": {
                "potential_leads": "中等",
                "attention_boost": "显著",
                "conversion_path": "新闻关注 -> GEO 报告 -> 服务咨询",
            },
            "content_angles": ["技术对比", "市场分析", "用户评价"],
            "risks": ["时效性风险", "竞争对手反应"],
            "next_steps": ["制作内容", "多渠道发布", "数据跟踪"],
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
