"""
AI 与产业互联网研究系统 - 配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 存储目录
STORAGE_DIR = BASE_DIR / "storage"
PAPERS_DIR = STORAGE_DIR / "papers"
NOTES_DIR = STORAGE_DIR / "notes"
ARTICLES_DIR = STORAGE_DIR / "articles"
NEWS_DIR = STORAGE_DIR / "news"

# 确保目录存在
for d in [PAPERS_DIR, NOTES_DIR, ARTICLES_DIR, NEWS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# API 配置
ARXIV_API_URL = "http://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"

# 搜索关键词
DEFAULT_KEYWORDS = [
    "artificial intelligence industry internet",
    "AI industrial applications",
    "machine learning manufacturing",
    "AI supply chain",
    "industrial IoT AI",
    "AI enterprise digitalization",
    "产业互联网 人工智能",
    "AI 产业应用",
    "智能制造 人工智能",
]

# 新闻源
NEWS_SOURCES = [
    "https://www.ainews.com/feed",
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
]

# 输出配置
OUTPUT_FORMAT = "markdown"
MAX_ARTICLE_LENGTH = 5000

# AI 模型配置（可选）
AI_MODEL = os.getenv("AI_MODEL", "qwen")
AI_API_KEY = os.getenv("AI_API_KEY", "")
