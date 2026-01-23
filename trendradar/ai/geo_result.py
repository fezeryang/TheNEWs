# coding=utf-8
"""
GEO 分析结果数据结构

定义 GEO 借势分析的结果数据类型
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class GEOEntity:
    """GEO 实体（品牌/产品/公司）"""
    name: str = ""                          # 实体名称
    type: str = ""                          # 实体类型：brand/product/company
    marketing_value: int = 0                # 营销价值评分 (0-100)
    value_reasons: List[str] = field(default_factory=list)  # 评分理由
    hotness_score: int = 0                  # 热度评分 (0-100)
    context: str = ""                       # 实体上下文


@dataclass
class ConversationBridge:
    """话术桥接"""
    hook: str = ""                          # 钩子：吸引注意力
    bridge: str = ""                        # 桥接：引出必要性
    cta: str = ""                           # 行动召唤：引导查看


@dataclass
class CompetitorAnalysis:
    """竞品对比分析"""
    brand: str = ""                         # 主品牌名称
    competitors: List[str] = field(default_factory=list)  # 竞品列表
    comparison_points: List[str] = field(default_factory=list)  # 对比维度
    differentiation: str = ""               # 核心差异化点


@dataclass
class GEORecommendation:
    """GEO 推荐建议"""
    recommended: bool = False               # 是否推荐
    priority: str = "low"                   # 优先级：high/medium/low
    confidence: float = 0.0                 # 信心度 (0.0-1.0)
    execution_plan: str = ""                # 执行计划
    expected_outcome: str = ""              # 预期效果


@dataclass
class GEOAnalysisResult:
    """GEO 分析结果"""
    # GEO 特定字段
    entities: List[GEOEntity] = field(default_factory=list)  # 识别的实体列表
    conversation_bridge: Optional[ConversationBridge] = None  # 话术桥接
    competitor_analysis: Optional[CompetitorAnalysis] = None  # 竞品分析
    geo_recommendation: Optional[GEORecommendation] = None    # GEO 推荐
    
    # 特殊情况处理
    no_entity_reason: str = ""              # 无实体原因
    
    # 基础元数据
    raw_response: str = ""                  # 原始响应
    success: bool = False                   # 是否成功
    error: str = ""                         # 错误信息
    
    # 新闻数量统计（与通用分析保持一致）
    total_news: int = 0                     # 总新闻数（热榜+RSS）
    analyzed_news: int = 0                  # 实际分析的新闻数
    max_news_limit: int = 0                 # 分析上限配置值
    hotlist_count: int = 0                  # 热榜新闻数
    rss_count: int = 0                      # RSS 新闻数
