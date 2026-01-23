#!/usr/bin/env python3
# coding=utf-8
"""
GEO 分析系统测试脚本

测试 GEO 趋势分析系统的各个模块
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from trendradar.ai.client import AIClient
from trendradar.geo import (
    EntityExtractor,
    MarketingValueAnalyzer,
    ConversationBridge,
    CompetitorAnalyzer,
    GEORecommendationEngine,
)


def test_entity_extraction():
    """测试实体识别模块"""
    print("\n" + "="*60)
    print("测试 1: 实体识别模块")
    print("="*60)
    
    # 模拟 AI 客户端（使用环境变量配置）
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 2000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  未设置 AI_API_KEY 环境变量，跳过测试")
        return False
    
    ai_client = AIClient(ai_config)
    extractor = EntityExtractor(ai_client, language="Chinese")
    
    # 测试新闻
    test_news = {
        "title": "西贝莜面村推出新品莜面套餐",
        "content": "西贝莜面村今日宣布推出全新莜面套餐系列，此举被认为是针对海底捞等竞品的差异化战略。",
    }
    
    print(f"\n测试新闻: {test_news['title']}")
    result = extractor.extract_entities(test_news["content"], test_news["title"])
    
    if result["success"]:
        print(f"✓ 成功识别 {len(result['entities'])} 个实体")
        for entity in result["entities"]:
            print(f"  - {entity['name']} ({entity['type']}) - 热度: {entity['hotness_score']}")
        return True
    else:
        print(f"✗ 识别失败: {result['error']}")
        return False


def test_marketing_value():
    """测试营销价值分析模块"""
    print("\n" + "="*60)
    print("测试 2: 营销价值分析模块")
    print("="*60)
    
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 2000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  未设置 AI_API_KEY 环境变量，跳过测试")
        return False
    
    ai_client = AIClient(ai_config)
    analyzer = MarketingValueAnalyzer(ai_client, language="Chinese")
    
    # 测试新闻
    test_news = {
        "title": "西贝莜面村推出新品莜面套餐",
        "content": "西贝莜面村今日宣布推出全新莜面套餐系列，此举被认为是针对海底捞等竞品的差异化战略。",
    }
    
    print(f"\n测试新闻: {test_news['title']}")
    result = analyzer.analyze_marketing_value(test_news["title"], test_news["content"])
    
    if result["success"]:
        print(f"✓ 营销价值评分: {result['score']}/100")
        print(f"  原因: {', '.join(result['reasons'])}")
        print(f"  营销角度: {result['marketing_angle']}")
        return True
    else:
        print(f"✗ 分析失败: {result['error']}")
        return False


def test_conversation_bridge():
    """测试话术桥接模块"""
    print("\n" + "="*60)
    print("测试 3: 话术桥接模块")
    print("="*60)
    
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.8,
        "MAX_TOKENS": 2000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  未设置 AI_API_KEY 环境变量，跳过测试")
        return False
    
    ai_client = AIClient(ai_config)
    bridge = ConversationBridge(ai_client, language="Chinese")
    
    # 测试数据
    test_data = {
        "title": "西贝莜面村推出新品莜面套餐",
        "summary": "西贝莜面村今日宣布推出全新莜面套餐系列",
        "brand": "西贝莜面村",
        "marketing_value": {
            "score": 85,
            "reasons": ["新品发布", "竞争策略"],
            "marketing_angle": "差异化创新",
        },
    }
    
    print(f"\n测试品牌: {test_data['brand']}")
    result = bridge.generate_bridge(
        test_data["title"],
        test_data["summary"],
        test_data["brand"],
        test_data["marketing_value"],
    )
    
    if result["success"]:
        print(f"✓ 生成 {len(result['templates'])} 套话术模板")
        for i, template in enumerate(result["templates"][:2], 1):
            print(f"\n  模板 {i} - {template['style']}:")
            print(f"    Hook: {template['hook'][:80]}...")
            print(f"    CTA: {template['call_to_action'][:80]}...")
        return True
    else:
        print(f"✗ 生成失败: {result['error']}")
        return False


def test_competitor_analysis():
    """测试竞品分析模块"""
    print("\n" + "="*60)
    print("测试 4: 竞品分析模块")
    print("="*60)
    
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 2000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  未设置 AI_API_KEY 环境变量，跳过测试")
        return False
    
    ai_client = AIClient(ai_config)
    analyzer = CompetitorAnalyzer(ai_client, language="Chinese")
    
    # 测试数据
    test_data = {
        "brand": "西贝莜面村",
        "industry": "餐饮",
        "context": "西贝莜面村推出新品莜面套餐，针对海底捞等竞品的差异化战略。",
    }
    
    print(f"\n测试品牌: {test_data['brand']}")
    result = analyzer.analyze_competitors(
        test_data["brand"],
        test_data["industry"],
        test_data["context"],
    )
    
    if result["success"]:
        print(f"✓ 识别 {len(result['competitors'])} 个竞品")
        for comp in result["competitors"]:
            print(f"  - {comp['name']}: {comp['reason']}")
        print(f"\n  对比维度: {len(result['comparison_dimensions'])} 个")
        return True
    else:
        print(f"✗ 分析失败: {result['error']}")
        return False


def test_geo_recommendation():
    """测试 GEO 推荐引擎（完整流程）"""
    print("\n" + "="*60)
    print("测试 5: GEO 推荐引擎（完整流程）")
    print("="*60)
    
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 3000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  未设置 AI_API_KEY 环境变量，跳过测试")
        return False
    
    ai_client = AIClient(ai_config)
    engine = GEORecommendationEngine(
        ai_client,
        language="Chinese",
        output_dir="/tmp/geo_test_output",
    )
    
    # 测试新闻列表
    test_news_list = [
        {
            "id": "test_1",
            "title": "西贝莜面村推出新品莜面套餐",
            "content": "西贝莜面村今日宣布推出全新莜面套餐系列，包含多款精选莜面和配菜组合。此举被行业分析师认为是针对海底捞、外婆家等竞品的差异化战略，旨在吸引更多年轻消费者。",
            "url": "https://example.com/news1",
        },
        {
            "id": "test_2",
            "title": "某不知名公司发布产品",
            "content": "某公司发布了一款新产品。",
            "url": "https://example.com/news2",
        },
    ]
    
    print(f"\n测试 {len(test_news_list)} 条新闻")
    
    # 批量分析
    results = engine.analyze_news_batch(test_news_list, max_news=2)
    
    # 统计结果
    recommended = [r for r in results if r.get("geo_recommendation", {}).get("recommended", False)]
    high_priority = engine.get_high_priority_recommendations(results)
    
    print(f"\n✓ 分析完成:")
    print(f"  - 总计: {len(results)} 条")
    print(f"  - 推荐: {len(recommended)} 条")
    print(f"  - 高优先级: {len(high_priority)} 条")
    
    # 保存结果
    output_file = engine.save_results(results, filename="test_results.json")
    print(f"\n✓ 结果已保存: {output_file}")
    
    return len(recommended) > 0


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("GEO 趋势分析系统 - 模块测试")
    print("="*60)
    
    # 检查 API Key
    if not os.getenv("AI_API_KEY"):
        print("\n⚠️  请设置 AI_API_KEY 环境变量")
        print("示例: export AI_API_KEY=your_api_key")
        print("\n如果需要测试其他模型，也可以设置 AI_MODEL 环境变量")
        print("示例: export AI_MODEL=openai/gpt-4")
        return
    
    print(f"\n使用模型: {os.getenv('AI_MODEL', 'deepseek/deepseek-chat')}")
    
    # 运行测试
    tests = [
        ("实体识别", test_entity_extraction),
        ("营销价值分析", test_marketing_value),
        ("话术桥接", test_conversation_bridge),
        ("竞品分析", test_competitor_analysis),
        ("GEO 推荐引擎", test_geo_recommendation),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n✗ {name} 测试异常: {e}")
            results[name] = False
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, passed_test in results.items():
        status = "✓ 通过" if passed_test else "✗ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！GEO 分析系统运行正常。")
    else:
        print("\n⚠️  部分测试失败，请检查配置和 AI API。")


if __name__ == "__main__":
    main()
