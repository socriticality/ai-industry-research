"""
新闻抓取器 - 获取 AI 和产业互联网相关新闻
"""
import feedparser
import requests
from datetime import datetime, timedelta
import json
from pathlib import Path
from config.settings import NEWS_DIR


class NewsScraper:
    """新闻抓取器"""
    
    def __init__(self):
        # AI 和科技新闻源
        self.sources = [
            {'name': 'AI News', 'url': 'https://www.ainews.com/feed'},
            {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/'},
            {'name': 'Wired', 'url': 'https://www.wired.com/feed/rss'},
            {'name': 'MIT Tech Review', 'url': 'https://www.technologyreview.com/feed/'},
            {'name': 'VentureBeat AI', 'url': 'https://venturebeat.com/category/ai/feed/'},
        ]
        
        # 关键词过滤
        self.keywords = [
            'artificial intelligence', 'AI', 'machine learning',
            'industry internet', 'industrial AI', 'enterprise AI',
            'digitalization', 'automation', 'smart manufacturing',
            '人工智能', '产业互联网', '智能制造', '数字化转型'
        ]
    
    def fetch_all(self, hours_back=24):
        """抓取所有新闻源"""
        all_news = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for source in self.sources:
            print(f"📰 抓取 {source['name']}...")
            try:
                response = requests.get(source['url'], timeout=15)
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries:
                    # 检查时间
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_time = datetime(*entry.published_parsed[:6])
                        if pub_time < cutoff_time:
                            continue
                    else:
                        pub_time = datetime.now()
                    
                    # 检查相关性
                    title = entry.title.lower()
                    summary = entry.summary.lower() if hasattr(entry, 'summary') else ''
                    
                    if self._is_relevant(title + ' ' + summary):
                        news_item = {
                            'title': entry.title,
                            'summary': entry.summary if hasattr(entry, 'summary') else '',
                            'link': entry.links[0].href if hasattr(entry, 'links') and entry.links else '',
                            'published': entry.published if hasattr(entry, 'published') else '',
                            'source': source['name'],
                            'captured_at': datetime.now().isoformat()
                        }
                        all_news.append(news_item)
                
            except Exception as e:
                print(f"  ✗ {source['name']} 抓取失败：{e}")
        
        print(f"\n✓ 共找到 {len(all_news)} 条相关新闻\n")
        return all_news
    
    def _is_relevant(self, text):
        """检查新闻是否与 AI/产业互联网相关"""
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in self.keywords)
    
    def save_news(self, news_items):
        """保存新闻到本地"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = NEWS_DIR / f"news_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'fetch_date': datetime.now().isoformat(),
                'total_news': len(news_items),
                'news': news_items
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已保存新闻到 {filename}")
        return filename


def fetch_latest_news(hours_back=24):
    """获取最新新闻的主函数"""
    scraper = NewsScraper()
    news = scraper.fetch_all(hours_back)
    
    if news:
        scraper.save_news(news)
    
    return news


if __name__ == "__main__":
    news = fetch_latest_news()
    for n in news[:5]:
        print(f"📰 {n['title']}")
        print(f"   来源：{n['source']} | {n['published']}\n")
