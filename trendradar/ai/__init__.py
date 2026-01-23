# coding=utf-8
"""
TrendRadar AI 模块

提供 AI 大模型对热点新闻的深度分析和翻译功能
"""

from .analyzer import AIAnalyzer, AIAnalysisResult
from .geo_analyzer import GEOAnalyzer
from .geo_result import GEOAnalysisResult, GEOEntity, ConversationBridge, CompetitorAnalysis, GEORecommendation
from .translator import AITranslator, TranslationResult, BatchTranslationResult
from .formatter import (
    get_ai_analysis_renderer,
    render_ai_analysis_markdown,
    render_ai_analysis_feishu,
    render_ai_analysis_dingtalk,
    render_ai_analysis_html,
    render_ai_analysis_html_rich,
    render_ai_analysis_plain,
    get_geo_analysis_renderer,
    render_geo_analysis_markdown,
    render_geo_analysis_feishu,
    render_geo_analysis_html,
)

__all__ = [
    # 分析器
    "AIAnalyzer",
    "AIAnalysisResult",
    # GEO 分析器
    "GEOAnalyzer",
    "GEOAnalysisResult",
    "GEOEntity",
    "ConversationBridge",
    "CompetitorAnalysis",
    "GEORecommendation",
    # 翻译器
    "AITranslator",
    "TranslationResult",
    "BatchTranslationResult",
    # 格式化
    "get_ai_analysis_renderer",
    "render_ai_analysis_markdown",
    "render_ai_analysis_feishu",
    "render_ai_analysis_dingtalk",
    "render_ai_analysis_html",
    "render_ai_analysis_html_rich",
    "render_ai_analysis_plain",
    # GEO 格式化
    "get_geo_analysis_renderer",
    "render_geo_analysis_markdown",
    "render_geo_analysis_feishu",
    "render_geo_analysis_html",
]
