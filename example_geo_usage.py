#!/usr/bin/env python3
# coding=utf-8
"""
GEO 分析系统使用示例

展示如何使用 GEO 系统分析新闻并生成营销推荐
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from trendradar.ai.client import AIClient
from trendradar.geo import GEORecommendationEngine


def example_1_simple_analysis():
    """示例 1: 简单的新闻分析"""
    print("\n" + "="*60)
    print("示例 1: 分析单条新闻")
    print("="*60)
    
    # 配置 AI 客户端
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 3000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  请设置 AI_API_KEY 环境变量")
        return
    
    # 创建 GEO 引擎
    engine = GEORecommendationEngine(
        ai_client=AIClient(ai_config),
        language="Chinese",
        output_dir="/tmp/geo_examples",
    )
    
    # 准备新闻
    news = {
        "id": "example_1",
        "title": "小米汽车SU7降价促销，挑战特斯拉Model 3",
        "content": """
        小米汽车今日宣布，旗下首款电动车SU7将推出限时优惠活动，
        起售价下调2万元。业内分析认为，此举是小米汽车针对特斯拉
        Model 3的直接挑战，意图在新能源汽车市场占据更大份额。
        小米汽车CEO雷军表示，SU7在智能驾驶和车机系统方面具有
        明显优势，价格下调将吸引更多消费者。
        """,
        "url": "https://example.com/xiaomi-su7",
    }
    
    print(f"\n📰 分析新闻: {news['title']}")
    
    # 执行分析
    result = engine.analyze_news(news)
    
    # 显示结果
    if result.get("geo_recommendation", {}).get("recommended"):
        print("\n✅ 推荐作为 GEO 营销机会")
        print(f"   优先级: {result['geo_recommendation']['priority']}")
        print(f"   信心分数: {result['geo_recommendation']['confidence_score']}")
        
        # 显示实体
        if result.get("entities"):
            print(f"\n📌 识别的实体:")
            for entity in result["entities"][:3]:
                print(f"   - {entity['name']} ({entity['type']}) - 热度: {entity['hotness_score']}")
        
        # 显示营销价值
        if result.get("marketing_value"):
            mv = result["marketing_value"]
            print(f"\n💰 营销价值: {mv['score']}/100")
            print(f"   角度: {mv.get('marketing_angle', 'N/A')}")
            print(f"   理由: {', '.join(mv.get('reasons', [])[:3])}")
        
        # 显示话术
        if result.get("conversation_bridge", {}).get("templates"):
            template = result["conversation_bridge"]["templates"][0]
            print(f"\n💬 话术示例 ({template['style']}):")
            print(f"   Hook: {template['hook'][:100]}...")
            print(f"   CTA: {template['call_to_action'][:100]}...")
    else:
        print("\n❌ 不推荐作为 GEO 营销机会")
        print(f"   原因: {result.get('skip_reason', '未知')}")


def example_2_batch_analysis():
    """示例 2: 批量分析多条新闻"""
    print("\n" + "="*60)
    print("示例 2: 批量分析多条新闻")
    print("="*60)
    
    # 配置 AI 客户端
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 3000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  请设置 AI_API_KEY 环境变量")
        return
    
    # 创建 GEO 引擎
    engine = GEORecommendationEngine(
        ai_client=AIClient(ai_config),
        language="Chinese",
        output_dir="/tmp/geo_examples",
    )
    
    # 准备新闻列表
    news_list = [
        {
            "id": "news_1",
            "title": "华为发布Mate 70系列，搭载全新麒麟芯片",
            "content": "华为今日正式发布Mate 70系列旗舰手机，搭载自研麒麟9010芯片...",
            "url": "https://example.com/huawei-mate70",
        },
        {
            "id": "news_2",
            "title": "美团外卖推出会员新政策",
            "content": "美团外卖宣布调整会员政策，新增更多权益...",
            "url": "https://example.com/meituan-policy",
        },
        {
            "id": "news_3",
            "title": "某地发生交通事故",
            "content": "今日某地发生一起交通事故，造成拥堵...",
            "url": "https://example.com/accident",
        },
    ]
    
    print(f"\n📰 准备分析 {len(news_list)} 条新闻")
    
    # 批量分析
    results = engine.analyze_news_batch(news_list, max_news=3)
    
    # 统计和展示
    recommended = [r for r in results if r.get("geo_recommendation", {}).get("recommended")]
    high_priority = engine.get_high_priority_recommendations(results)
    
    print(f"\n📊 分析结果:")
    print(f"   总计: {len(results)} 条")
    print(f"   推荐: {len(recommended)} 条")
    print(f"   高优先级: {len(high_priority)} 条")
    
    # 显示高优先级推荐
    if high_priority:
        print(f"\n🔥 高优先级营销机会:")
        for i, rec in enumerate(high_priority, 1):
            print(f"\n   {i}. {rec['title']}")
            print(f"      品牌: {rec.get('main_brand', 'N/A')}")
            print(f"      营销分数: {rec.get('marketing_value', {}).get('score', 0)}")
            print(f"      推荐理由: {', '.join(rec.get('marketing_value', {}).get('reasons', [])[:2])}")
    
    # 保存结果
    output_file = engine.save_results(results, filename="batch_example.json")
    print(f"\n💾 结果已保存: {output_file}")


def example_3_filtering():
    """示例 3: 使用过滤器筛选高价值新闻"""
    print("\n" + "="*60)
    print("示例 3: 筛选高价值新闻")
    print("="*60)
    
    # 配置 AI 客户端
    ai_config = {
        "MODEL": os.getenv("AI_MODEL", "deepseek/deepseek-chat"),
        "API_KEY": os.getenv("AI_API_KEY", ""),
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 3000,
    }
    
    if not ai_config["API_KEY"]:
        print("⚠️  请设置 AI_API_KEY 环境变量")
        return
    
    # 创建 GEO 引擎
    engine = GEORecommendationEngine(
        ai_client=AIClient(ai_config),
        language="Chinese",
        output_dir="/tmp/geo_examples",
    )
    
    # 模拟已分析的新闻
    news_list = [
        {
            "id": "news_1",
            "title": "字节跳动推出AI编程助手",
            "content": "字节跳动今日发布AI编程助手Coze，挑战GitHub Copilot...",
            "url": "https://example.com/bytedance-ai",
        },
    ]
    
    print(f"\n📰 分析新闻并应用过滤器")
    
    # 分析
    results = engine.analyze_news_batch(news_list, max_news=1)
    
    # 应用过滤器
    # 1. 营销价值 >= 70 分
    high_value = [
        r for r in results
        if r.get("marketing_value", {}).get("score", 0) >= 70
    ]
    
    # 2. 必须包含品牌实体
    with_brands = [
        r for r in results
        if any(e.get("type") in ["brand", "company"] for e in r.get("entities", []))
    ]
    
    # 3. 推荐且高优先级
    high_priority_recommended = [
        r for r in results
        if r.get("geo_recommendation", {}).get("recommended")
        and r.get("geo_recommendation", {}).get("priority") == "high"
    ]
    
    print(f"\n📊 过滤结果:")
    print(f"   原始新闻: {len(results)} 条")
    print(f"   营销价值 ≥ 70: {len(high_value)} 条")
    print(f"   包含品牌实体: {len(with_brands)} 条")
    print(f"   高优先级推荐: {len(high_priority_recommended)} 条")


def main():
    """运行示例"""
    print("\n" + "="*60)
    print("GEO 趋势分析系统 - 使用示例")
    print("="*60)
    
    # 检查 API Key
    if not os.getenv("AI_API_KEY"):
        print("\n⚠️  请设置 AI_API_KEY 环境变量")
        print("示例: export AI_API_KEY=your_api_key")
        print("\n如需使用其他模型，设置 AI_MODEL 环境变量")
        print("示例: export AI_MODEL=openai/gpt-4")
        return
    
    print(f"\n使用模型: {os.getenv('AI_MODEL', 'deepseek/deepseek-chat')}")
    print("\n提示: 本示例会调用 AI API，请确保有足够的配额")
    
    try:
        # 运行示例
        example_1_simple_analysis()
        
        # 可选：取消注释以运行更多示例
        # example_2_batch_analysis()
        # example_3_filtering()
        
        print("\n" + "="*60)
        print("示例完成！")
        print("="*60)
        print("\n💡 提示:")
        print("  - 查看 /tmp/geo_examples/ 目录下的 JSON 结果文件")
        print("  - 修改代码中的新闻内容来测试不同场景")
        print("  - 参考 GEO_README.md 了解更多用法")
        
    except Exception as e:
        print(f"\n❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
