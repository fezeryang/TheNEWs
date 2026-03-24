---
name: trendradar-patterns
description: Coding patterns extracted from TrendRadar repository
version: 1.0.0
source: local-git-analysis
analyzed_commits: 7
---

# TrendRadar Coding Patterns

## Project Overview

TrendRadar is a Python-based hot news aggregation and analysis tool that uses AI to analyze trending topics from various Chinese platforms. The project features a modular architecture with support for GEO (Growth through Event Opportunities) marketing analysis.

## Commit Conventions

This project uses **imperative commit messages** without strict conventional commit prefixes:

- `Add ...` - New features or components
- `Complete ...` - Finishing implementation
- `Initial ...` - First-time setup

Examples from recent commits:
- `Add .gitignore to exclude Python cache files`
- `Complete GEO analysis system implementation with testing`
- `Add GEO analysis system: prompt, analyzer, renderer and config`
- `Initial plan`

## Code Architecture

```
trendradar/
├── __init__.py           # Package init
├── __main__.py           # Main entry point (NewsAnalyzer class)
├── context.py            # AppContext - application state management
│
├── ai/                   # AI analysis modules
│   ├── analyzer.py       # AIAnalyzer, AIAnalysisResult (GEO mode support)
│   ├── client.py         # AIClient - LiteLLM wrapper
│   ├── formatter.py      # AI output formatting
│   └── translator.py     # Translation functionality
│
├── content/              # Content generation modules (GEO)
│   ├── manager.py        # ContentManager - saves generated content
│   └── renderer.py       # Renders content for xiaohongshu/wechat
│
├── core/                 # Core analysis logic
│   ├── analyzer.py       # Frequency analysis, keyword matching
│   ├── config.py         # load_config()
│   ├── data.py           # Data structures
│   ├── frequency.py      # Frequency word matching
│   └── loader.py         # Configuration loading
│
├── crawler/              # Web scraping
│   ├── fetcher.py        # DataFetcher - hotlist crawling
│   └── rss/              # RSS feed handling
│       ├── fetcher.py    # RSSFetcher
│       └── parser.py     # RSS parsing
│
├── notification/         # Multi-channel notifications
│   ├── dispatcher.py     # NotificationDispatcher
│   ├── formatters.py     # Message formatting
│   ├── push_manager.py   # Push window control
│   ├── renderer.py       # Notification rendering
│   ├── senders.py        # Individual channel senders
│   └── batch.py          # Batch message handling
│
├── report/               # HTML report generation
│   ├── generator.py      # Report generation
│   ├── html.py           # HTML rendering
│   ├── rss_html.py       # RSS-specific HTML
│   └── helpers.py        # Report utilities
│
├── storage/              # Data persistence
│   ├── manager.py        # StorageManager
│   ├── base.py           # Base storage interface
│   ├── local.py          # Local file storage
│   ├── remote.py         # S3-compatible remote storage
│   └── sqlite_mixin.py   # SQLite database operations
│
└── utils/                # Utilities
    ├── time.py           # Timezone helpers
    └── url.py            # URL utilities

config/
├── config.yaml           # Main configuration
├── frequency_words.txt   # Keyword groups for filtering
├── ai_analysis_prompt.txt      # Generic AI prompt
└── ai_analysis_geo_prompt.txt  # GEO marketing prompt
```

## Design Patterns

### 1. Context Pattern (`AppContext`)
Centralized state management passed around to avoid globals:
```python
self.ctx = AppContext(config)
self.ctx.get_time()
self.ctx.format_date()
self.ctx.create_notification_dispatcher()
```

### 2. Dataclass Results
Using `@dataclass` for structured return values:
```python
@dataclass
class AIAnalysisResult:
    analysis_mode: str = "generic"
    is_safe: bool = True
    xiaohongshu_content: Optional[Dict[str, Any]] = None
    wechat_article: Optional[Dict[str, Any]] = None
    # ... more fields
```

### 3. Strategy Pattern for AI Analysis
Different analysis modes (generic vs geo) with unified interface:
```python
def analyze(...) -> AIAnalysisResult:
    # Generic mode

def analyze_hotspot(...) -> AIAnalysisResult:
    # Hotspot mode (no keyword filtering)
```

### 4. Manager Pattern
Managers handle complex operations with multiple steps:
- `ContentManager` - Save generated content to files
- `StorageManager` - Handle multiple storage backends
- `PushManager` - Time-based push window control

## Workflows

### Adding a New AI Analysis Mode

1. **Create prompt template** in `config/ai_analysis_{mode}_prompt.txt`
2. **Update `AIAnalyzer`** in `trendradar/ai/analyzer.py`:
   - Add new `analyze_*` method
   - Update `_parse_response` for new response format
3. **Update `AIAnalysisResult`** dataclass with new fields
4. **Add config options** in `config/config.yaml` under `ai_analysis`

### Adding Content Generation (GEO Mode)

1. **Add content fields** to prompt template JSON response
2. **Update `AIAnalysisResult`** with new content fields
3. **Create renderer** in `trendradar/content/renderer.py`
4. **Create manager** in `trendradar/content/manager.py`
5. **Integrate** in `__main__.py`:
   ```python
   from trendradar.content import ContentManager

   def _save_generated_content(self, ai_result, date_folder):
       content_manager = ContentManager()
       paths = content_manager.save_all_content(ai_result, date_folder)
   ```

### Adding a New Notification Channel

1. **Create sender** in `trendradar/notification/senders.py`
2. **Update dispatcher** in `trendradar/notification/dispatcher.py`
3. **Add config** in `config/config.yaml` under `notification.channels`
4. **Add webhooks** to `_has_notification_configured()` in `__main__.py`

## Configuration Patterns

### YAML Structure
```yaml
# Feature toggles
enabled: true/false

# Mode selection
mode: "generic" | "geo"

# Sub-feature configs
hotspot_mode: false
hotspot_max_count: 30

# Platform/source lists
sources:
  - id: "platform-id"
    name: "Display Name"
```

### Environment Variable Overrides
```python
env_var = os.environ.get("API_KEY", "") or config.get("api_key", "")
```

## File Naming Conventions

| Pattern | Usage | Example |
|---------|-------|---------|
| `__init__.py` | Package markers | Every subdirectory |
| `__main__.py` | Entry points | `trendradar/__main__.py` |
| `manager.py` | Coordinators | `storage/manager.py` |
| `formatter.py` | Output formatting | `ai/formatter.py` |
| `renderer.py` | Template rendering | `notification/renderer.py` |
| `{module}_prompt.txt` | AI prompts | `ai_analysis_geo_prompt.txt` |

## Testing Patterns

Currently uses manual testing with `DEBUG` mode:
```yaml
advanced:
  debug: true  # Enables detailed logging
```

## Python Version and Dependencies

- **Python**: 3.12+
- **Key dependencies**: LiteLLM (AI), feedparser (RSS), requests (HTTP)
- **Encoding**: Always use `encoding="utf-8"` for file operations

## Error Handling Patterns

```python
try:
    # Operation
except SpecificException as e:
    # Log friendly message
    print(f"[Module] Operation failed: {e}")
    # Return safe default
    return default_value
except Exception as e:
    # Log detailed error in non-user-facing output
    import traceback
    traceback.print_exc(file=sys.stderr)
```

## GEO Analysis System (New Feature)

The GEO (Growth through Event Opportunities) system converts trending news into marketing opportunities:

**Key Components:**
1. **Safety Check** - AI filters out political/sensitive content
2. **Entity Recognition** - Identifies brands, products, industries
3. **Marketing Value** - Scores 0-100 on opportunity potential
4. **Content Generation** - Creates xiaohongshu posts and WeChat articles

**Configuration:**
```yaml
ai_analysis:
  mode: "geo"              # Enable GEO mode
  hotspot_mode: true       # Skip keyword filtering
  hotspot_max_count: 30    # Analyze top 30 hot news
```

**Output:**
- `output/content/xiaohongshu/{date}/` - Social media posts
- `output/content/wechat/{date}/` - Articles
- `output/content/prompts/{date}/` - Image generation prompts
