---
name: trendradar-geo-system
description: Complete GEO (Growth through Event Opportunities) marketing analysis system - convert trending news into marketing opportunities
version: 1.0.0
author: TrendRadar
tags: [ai, marketing, content-generation, hot-news, python]
url: https://github.com/sansan0/TrendRadar
---

# TrendRadar GEO Analysis System

A complete system for converting trending hot news into marketing opportunities through AI analysis. Generate ready-to-publish content for Xiaohongshu (Little Red Book) and WeChat Official Accounts.

## What This Skill Provides

### 1. Safety-First Content Analysis
AI automatically filters out:
- Political sensitive content
- Social negative events
- Legal risks
- Controversial topics
- Inappropriate gossip

### 2. Marketing Opportunity Detection
- **Entity Recognition**: Identifies brands, products, industries, technologies
- **Marketing Value Score**: 0-100 rating on opportunity potential
- **Competitor Analysis**: Identifies and compares competing brands
- **Conversation Bridge**: Designs natural "Hook → Bridge → CTA" funnels

### 3. Ready-to-Publish Content Generation
- **Xiaohongshu Notes**: 300-500 chars with emojis, hashtags, image prompts
- **WeChat Articles**: 800-1500 chars with Markdown formatting
- **AI Image Prompts**: Midjourney/Stable Diffusion compatible

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Hot News Sources                        │
│  (Toutiao, Weibo, Zhihu, Bilibili, Douyin, etc.)          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Hotspot News Selector                          │
│  Top N ranked news (no keyword filtering needed)            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 AI Safety Check                             │
│  Filter: Political, Negative, Legal, Controversial         │
└────────────────────────┬────────────────────────────────────┘
                         │ (safe content)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              GEO Marketing Analysis                         │
│  • Entity Recognition (brands, products, industries)        │
│  • Marketing Value Scoring (0-100)                          │
│  • Conversation Bridge (Hook → Bridge → CTA)               │
│  • Competitor Analysis                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               Content Generation                            │
│  • Xiaohongshu: 15-25 char title + 300-500 char body       │
│  • WeChat: 20-30 char title + 800-1500 char article        │
│  • Image Prompts: Midjourney/SD compatible                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Output Files                               │
│  output/content/xiaohongshu/{date}/                        │
│  output/content/wechat/{date}/                             │
│  output/content/prompts/{date}/                            │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Patterns

### AI Analysis Result Dataclass

```python
@dataclass
class AIAnalysisResult:
    # Mode identifier
    analysis_mode: str = "geo"

    # Safety check (required first)
    is_safe: bool = True
    blocked_categories: List[str] = field(default_factory=list)
    safety_reasoning: str = ""

    # Generated content
    xiaohongshu_content: Optional[Dict[str, Any]] = None
    wechat_article: Optional[Dict[str, Any]] = None

    # Full GEO data
    geo_data: Optional[Dict[str, Any]] = None
```

### Hotspot Analysis Method

```python
def analyze_hotspot(
    hotspot_news: List[Dict],  # Top N hot news, no keyword filtering
    report_mode: str = "hotspot",
    report_type: str = "热点借势分析",
) -> AIAnalysisResult:
    """Analyze trending news directly without keyword matching"""
    # 1. Format news for AI
    # 2. Call AI with GEO prompt
    # 3. Parse safety check first
    # 4. If safe, extract content generation
    # 5. Return result
```

### Content Saving Pattern

```python
def _save_generated_content(ai_result, date_folder):
    """Save generated content to organized file structure"""
    if not ai_result.is_safe:
        return  # Skip unsafe content

    content_manager = ContentManager(output_dir="output/content")
    paths = content_manager.save_all_content(ai_result, date_folder)

    # Creates:
    # - output/content/xiaohongshu/{date}/HHMMSS_title.md
    # - output/content/wechat/{date}/HHMMSS_title.md
    # - output/content/prompts/{date}/HHMMSS_platform_topic.txt
```

## AI Prompt Structure

### System Prompt
```
You are a Marketing Opportunity Analyst specializing in converting
public hot news into business opportunities.

## Safety First Principles (ALWAYS CHECK FIRST)

Content that is ABSOLUTELY NOT suitable:
- Political sensitive (government, policies, political conflicts)
- Social negative (accidents, disasters, crime)
- Legal risks (lawsuits, regulatory penalties)
- Controversial topics (religion, race, gender)

Safe content types:
- ✅ Commercial brands: product launches, marketing, competition
- ✅ Tech products: new features, user experience
- ✅ Industry trends: market changes, business models
```

### Response Format
```json
{
  "analysis_mode": "geo",
  "safety_check": {
    "is_safe": true|false,
    "blocked_categories": [],
    "reasoning": "explanation"
  },
  "entities": [...],
  "marketing_value": {
    "score": 0-100,
    "overall_rating": "high|medium|low|not_suitable"
  },
  "xiaohongshu_content": {
    "title": "🔥 15-25 chars with emoji",
    "body": "300-500 chars, casual style",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "image_prompt": "English prompt for Midjourney --ar 3:4"
  },
  "wechat_article": {
    "title": "20-30 chars",
    "summary": "50-80 chars",
    "body": "Markdown 800-1500 chars",
    "image_prompt": "Infographic style --ar 16:9"
  }
}
```

## Configuration

```yaml
ai_analysis:
  enabled: true
  mode: "geo"                    # Use GEO mode
  hotspot_mode: true             # Skip keyword filtering
  hotspot_max_count: 30          # Analyze top 30 hot news
  language: "Chinese"
  prompt_file: "ai_analysis_geo_prompt.txt"
  max_news_for_analysis: 50
```

## Output File Structure

```
output/content/
├── xiaohongshu/
│   └── 2026-01-23/
│       ├── 093015_小米汽车降价促销.md
│       └── 103045_DeepSeek突破性进展.md
├── wechat/
│   └── 2026-01-23/
│       ├── 093015_小米汽车降价促销.md
│       └── 103045_DeepSeek突破性进展.md
└── prompts/
    └── 2026-01-23/
        ├── 093015_xiaohongshu_小米汽车.md
        └── 103045_wechat_小米汽车.md
```

## Usage Example

```python
from trendradar.ai import AIAnalyzer
from trendradar.content import ContentManager

# Get hot news (top 30)
hot_news = get_hotspot_news(results, id_to_name, max_count=30)

# Analyze with AI
analyzer = AIAnalyzer(ai_config, analysis_config, get_time_func)
result = analyzer.analyze_hotspot(hot_news)

# Check safety
if result.is_safe:
    # Save generated content
    content_manager = ContentManager()
    paths = content_manager.save_all_content(result, date_folder)
    print(f"Saved: {paths}")
else:
    print(f"Content blocked: {result.safety_reasoning}")
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Safety First** | AI filters inappropriate content before generation |
| **No Keywords Needed** | Works with any hot news, not just pre-defined topics |
| **Ready to Publish** | Content formatted for each platform's requirements |
| **Image Prompts** | AI art prompts included for visuals |
| **File Organization** | Auto-organized by date and platform |

## Platform-Specific Formats

### Xiaohongshu (Little Red Book)
- **Title**: 15-25 chars, emoji, question/exclamation style
- **Body**: 300-500 chars, casual, emoji usage, bullet points
- **Tags**: 5 hashtags (industry + brand + generic)
- **Image**: Bright colors, minimal style, 3:4 ratio

### WeChat Official Account
- **Title**: 20-30 chars, professional but attractive
- **Summary**: 50-80 chars abstract
- **Body**: 800-1500 chars, Markdown structure with sections
- **Image**: Infographic style, data visualization, 16:9 ratio

## Dependencies

- **Python**: 3.12+
- **LiteLLM**: Multi-provider AI interface
- **feedparser**: RSS parsing
- **requests**: HTTP requests

## License

Same as parent TrendRadar project.
