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
        seen_urls = set()  # 去重
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for source in self.sources:
            print(f"📰 抓取 {source['name']}...")
            try:
                response = requests.get(source['url'], timeout=20)
                if response.status_code != 200:
                    print(f"  ⚠️  {source['name']} 返回状态码：{response.status_code}")
                    continue
                    
                feed = feedparser.parse(response.content)
                source_count = 0
                
                for entry in feed.entries:
                    # 检查时间
                    pub_time = self._parse_entry_time(entry)
                    if pub_time < cutoff_time:
                        continue
                    
                    # 检查相关性
                    title = entry.title.lower()
                    summary = entry.summary.lower() if hasattr(entry, 'summary') else ''
                    
                    if not self._is_relevant(title + ' ' + summary):
                        continue
                    
                    # 去重检查
                    article_url = entry.links[0].href if hasattr(entry, 'links') and entry.links else ''
                    if article_url in seen_urls:
                        continue
                    seen_urls.add(article_url)
                    
                    news_item = {
                        'title': entry.title,
                        'summary': entry.summary if hasattr(entry, 'summary') else '',
                        'link': article_url,
                        'published': entry.published if hasattr(entry, 'published') else '',
                        'source': source['name'],
                        'captured_at': datetime.now().isoformat()
                    }
                    all_news.append(news_item)
                    source_count += 1
                
                if source_count > 0:
                    print(f"  ✓ {source['name']}: {source_count} 条")
                
            except requests.exceptions.Timeout:
                print(f"  ✗ {source['name']} 超时")
            except requests.exceptions.RequestException as e:
                print(f"  ✗ {source['name']} 网络错误：{e}")
            except Exception as e:
                print(f"  ✗ {source['name']} 错误：{e}")
        
        print(f"\n✓ 共找到 {len(all_news)} 条独特相关新闻\n")
        return all_news
    
    def _parse_entry_time(self, entry):
        """解析新闻条目时间"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                return datetime(*entry.published_parsed[:6])
            except (TypeError, IndexError):
                pass
        if hasattr(entry, 'published'):
            try:
                # 尝试解析常见日期格式
                pub_str = entry.published
                if 'GMT' in pub_str or '+' in pub_str:
                    # RFC 2822 格式
                    from email.utils import parsedate_to_datetime
                    return parsedate_to_datetime(pub_str).replace(tzinfo=None)
            except:
                pass
        return datetime.now()
    
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
