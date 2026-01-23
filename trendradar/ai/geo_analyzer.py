# coding=utf-8
"""
GEO 分析器模块

专门用于品牌营销借势分析
基于 LiteLLM 统一接口，支持 100+ AI 提供商
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from trendradar.ai.client import AIClient
from trendradar.ai.geo_result import (
    GEOAnalysisResult,
    GEOEntity,
    ConversationBridge,
    CompetitorAnalysis,
    GEORecommendation,
)


class GEOAnalyzer:
    """GEO 分析器 - 专门用于品牌营销借势分析"""

    def __init__(
        self,
        ai_config: Dict[str, Any],
        analysis_config: Dict[str, Any],
        get_time_func: Callable,
        debug: bool = False,
    ):
        """
        初始化 GEO 分析器

        Args:
            ai_config: AI 模型配置（LiteLLM 格式）
            analysis_config: AI 分析功能配置（language, prompt_file 等）
            get_time_func: 获取当前时间的函数
            debug: 是否开启调试模式
        """
        self.ai_config = ai_config
        self.analysis_config = analysis_config
        self.get_time_func = get_time_func
        self.debug = debug

        # 创建 AI 客户端（基于 LiteLLM）
        self.client = AIClient(ai_config)

        # 验证配置
        valid, error = self.client.validate_config()
        if not valid:
            print(f"[GEO] 配置警告: {error}")

        # 从分析配置获取功能参数
        self.max_news = analysis_config.get("MAX_NEWS_FOR_ANALYSIS", 50)
        self.include_rss = analysis_config.get("INCLUDE_RSS", True)
        self.include_rank_timeline = analysis_config.get("INCLUDE_RANK_TIMELINE", False)
        self.language = analysis_config.get("LANGUAGE", "Chinese")
        
        # GEO 特定配置
        geo_config = analysis_config.get("GEO", {})
        self.max_entities = geo_config.get("MAX_ENTITIES", 5)
        self.min_marketing_score = geo_config.get("MIN_MARKETING_SCORE", 60)
        self.brands_filter = geo_config.get("BRANDS_FILTER", [])

        # 加载提示词模板
        self.system_prompt, self.user_prompt_template = self._load_prompt_template(
            analysis_config.get("PROMPT_FILE", "ai_geo_prompt.txt")
        )

    def _load_prompt_template(self, prompt_file: str) -> tuple:
        """加载提示词模板"""
        config_dir = Path(__file__).parent.parent.parent / "config"
        prompt_path = config_dir / prompt_file

        if not prompt_path.exists():
            print(f"[GEO] 提示词文件不存在: {prompt_path}")
            return "", ""

        content = prompt_path.read_text(encoding="utf-8")

        # 解析 [system] 和 [user] 部分
        system_prompt = ""
        user_prompt = ""

        if "[system]" in content and "[user]" in content:
            parts = content.split("[user]")
            system_part = parts[0]
            user_part = parts[1] if len(parts) > 1 else ""

            # 提取 system 内容
            if "[system]" in system_part:
                system_prompt = system_part.split("[system]")[1].strip()

            user_prompt = user_part.strip()
        else:
            # 整个文件作为 user prompt
            user_prompt = content

        return system_prompt, user_prompt

    def analyze(
        self,
        stats: List[Dict],
        rss_stats: Optional[List[Dict]] = None,
        report_mode: str = "daily",
        report_type: str = "当日汇总",
        platforms: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
    ) -> GEOAnalysisResult:
        """
        执行 GEO 分析

        Args:
            stats: 热榜统计数据
            rss_stats: RSS 统计数据
            report_mode: 报告模式
            report_type: 报告类型
            platforms: 平台列表
            keywords: 关键词列表

        Returns:
            GEOAnalysisResult: GEO 分析结果
        """
        if not self.client.api_key:
            return GEOAnalysisResult(
                success=False,
                error="未配置 AI API Key，请在 config.yaml 或环境变量 AI_API_KEY 中设置"
            )

        # 准备新闻内容并获取统计数据
        news_content, rss_content, hotlist_total, rss_total, analyzed_count = self._prepare_news_content(stats, rss_stats)
        total_news = hotlist_total + rss_total

        if not news_content and not rss_content:
            return GEOAnalysisResult(
                success=False,
                error="没有可分析的新闻内容",
                total_news=total_news,
                hotlist_count=hotlist_total,
                rss_count=rss_total,
                analyzed_news=0,
                max_news_limit=self.max_news
            )

        # 构建提示词
        current_time = self.get_time_func().strftime("%Y-%m-%d %H:%M:%S")

        # 提取关键词
        if not keywords:
            keywords = [s.get("word", "") for s in stats if s.get("word")] if stats else []

        # 使用安全的字符串替换
        user_prompt = self.user_prompt_template
        user_prompt = user_prompt.replace("{report_mode}", report_mode)
        user_prompt = user_prompt.replace("{report_type}", report_type)
        user_prompt = user_prompt.replace("{current_time}", current_time)
        user_prompt = user_prompt.replace("{news_count}", str(hotlist_total))
        user_prompt = user_prompt.replace("{rss_count}", str(rss_total))
        user_prompt = user_prompt.replace("{platforms}", ", ".join(platforms) if platforms else "多平台")
        user_prompt = user_prompt.replace("{keywords}", ", ".join(keywords[:20]) if keywords else "无")
        user_prompt = user_prompt.replace("{news_content}", news_content)
        user_prompt = user_prompt.replace("{rss_content}", rss_content)
        user_prompt = user_prompt.replace("{language}", self.language)

        if self.debug:
            print("\n" + "=" * 80)
            print("[GEO 调试] 发送给 AI 的完整提示词")
            print("=" * 80)
            if self.system_prompt:
                print("\n--- System Prompt ---")
                print(self.system_prompt)
            print("\n--- User Prompt ---")
            print(user_prompt)
            print("=" * 80 + "\n")

        # 调用 AI API（使用 LiteLLM）
        try:
            response = self._call_ai(user_prompt)
            result = self._parse_response(response)

            # 填充统计数据
            result.total_news = total_news
            result.hotlist_count = hotlist_total
            result.rss_count = rss_total
            result.analyzed_news = analyzed_count
            result.max_news_limit = self.max_news
            return result
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)

            # 截断过长的错误消息
            if len(error_msg) > 200:
                error_msg = error_msg[:200] + "..."
            friendly_msg = f"GEO 分析失败 ({error_type}): {error_msg}"

            return GEOAnalysisResult(
                success=False,
                error=friendly_msg
            )

    def _prepare_news_content(
        self,
        stats: List[Dict],
        rss_stats: Optional[List[Dict]] = None,
    ) -> tuple:
        """
        准备新闻内容文本（复用通用分析器的逻辑）

        Returns:
            tuple: (news_content, rss_content, hotlist_total, rss_total, analyzed_count)
        """
        # 导入通用分析器的方法
        from trendradar.ai.analyzer import AIAnalyzer
        
        # 创建临时通用分析器实例以复用其 _prepare_news_content 方法
        temp_analyzer = AIAnalyzer(
            self.ai_config,
            self.analysis_config,
            self.get_time_func,
            self.debug
        )
        
        return temp_analyzer._prepare_news_content(stats, rss_stats)

    def _call_ai(self, user_prompt: str) -> str:
        """调用 AI API（使用 LiteLLM）"""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        return self.client.chat(messages)

    def _parse_response(self, response: str) -> GEOAnalysisResult:
        """解析 AI 响应"""
        result = GEOAnalysisResult(raw_response=response)

        if not response or not response.strip():
            result.error = "AI 返回空响应"
            return result

        # 尝试解析 JSON
        try:
            # 提取 JSON 部分
            json_str = response

            if "```json" in response:
                parts = response.split("```json", 1)
                if len(parts) > 1:
                    code_block = parts[1]
                    end_idx = code_block.find("```")
                    if end_idx != -1:
                        json_str = code_block[:end_idx]
                    else:
                        json_str = code_block
            elif "```" in response:
                parts = response.split("```", 2)
                if len(parts) >= 2:
                    json_str = parts[1]

            json_str = json_str.strip()
            if not json_str:
                raise ValueError("提取的 JSON 内容为空")

            data = json.loads(json_str)

            # 解析 GEO 分析结果
            geo_data = data.get("geo_analysis", {})
            
            # 解析实体列表
            entities_data = geo_data.get("entities", [])
            entities = []
            for entity_dict in entities_data:
                entity = GEOEntity(
                    name=entity_dict.get("name", ""),
                    type=entity_dict.get("type", ""),
                    marketing_value=entity_dict.get("marketing_value", 0),
                    value_reasons=entity_dict.get("value_reasons", []),
                    hotness_score=entity_dict.get("hotness_score", 0),
                    context=entity_dict.get("context", "")
                )
                entities.append(entity)
            result.entities = entities
            
            # 解析话术桥接
            bridge_data = geo_data.get("conversation_bridge")
            if bridge_data:
                result.conversation_bridge = ConversationBridge(
                    hook=bridge_data.get("hook", ""),
                    bridge=bridge_data.get("bridge", ""),
                    cta=bridge_data.get("cta", "")
                )
            
            # 解析竞品分析
            competitor_data = geo_data.get("competitor_analysis")
            if competitor_data:
                result.competitor_analysis = CompetitorAnalysis(
                    brand=competitor_data.get("brand", ""),
                    competitors=competitor_data.get("competitors", []),
                    comparison_points=competitor_data.get("comparison_points", []),
                    differentiation=competitor_data.get("differentiation", "")
                )
            
            # 解析推荐建议
            recommendation_data = geo_data.get("geo_recommendation", {})
            result.geo_recommendation = GEORecommendation(
                recommended=recommendation_data.get("recommended", False),
                priority=recommendation_data.get("priority", "low"),
                confidence=recommendation_data.get("confidence", 0.0),
                execution_plan=recommendation_data.get("execution_plan", ""),
                expected_outcome=recommendation_data.get("expected_outcome", "")
            )
            
            # 特殊情况
            result.no_entity_reason = geo_data.get("no_entity_reason", "")
            
            result.success = True

        except json.JSONDecodeError as e:
            error_context = json_str[max(0, e.pos - 30):e.pos + 30] if json_str and e.pos else ""
            result.error = f"JSON 解析错误 (位置 {e.pos}): {e.msg}"
            if error_context:
                result.error += f"，上下文: ...{error_context}..."
        except (IndexError, KeyError, TypeError, ValueError) as e:
            result.error = f"响应解析错误: {type(e).__name__}: {str(e)}"
        except Exception as e:
            result.error = f"解析时发生未知错误: {type(e).__name__}: {str(e)}"

        return result
