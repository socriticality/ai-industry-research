"""
论文抓取器 - 从 arXiv 和 Semantic Scholar 获取最新论文
"""
import feedparser
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
from config.settings import ARXIV_API_URL, PAPERS_DIR, DEFAULT_KEYWORDS


class ArXivScraper:
    """arXiv 论文抓取器"""
    
    def __init__(self, max_results=50, timeout=60):
        self.max_results = max_results
        self.base_url = ARXIV_API_URL
        self.timeout = timeout
    
    def _parse_date(self, date_str):
        """解析 arXiv 日期字符串"""
        if not date_str:
            return None
        try:
            # arXiv 日期格式：2026-03-05T18:52:28Z
            return datetime.strptime(date_str[:10], '%Y-%m-%d')
        except (ValueError, TypeError):
            return None
    
    def search(self, keywords, days_back=7):
        """搜索论文"""
        papers = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for keyword in keywords:
            # 构建搜索查询 - 按提交日期排序
            query = f"all:{keyword}"
            url = f"{self.base_url}?search_query={query}&start=0&max_results={self.max_results}&sortBy=submittedDate&sortOrder=descending"
            
            try:
                response = requests.get(url, timeout=self.timeout)
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries:
                    # 日期过滤
                    pub_date = self._parse_date(entry.published)
                    if pub_date and pub_date < cutoff_date:
                        continue  # 跳过超过时间范围的论文
                    
                    paper = {
                        'title': entry.title,
                        'authors': [author.name for author in entry.authors] if hasattr(entry, 'authors') else [],
                        'summary': entry.summary if hasattr(entry, 'summary') else '',
                        'published': entry.published if hasattr(entry, 'published') else '',
                        'updated': entry.updated if hasattr(entry, 'updated') else '',
                        'link': entry.links[0].href if hasattr(entry, 'links') and entry.links else '',
                        'pdf_link': self._get_pdf_link(entry),
                        'categories': [tag.term for tag in entry.tags] if hasattr(entry, 'tags') else [],
                        'source': 'arXiv',
                        'search_keyword': keyword,
                        'captured_at': datetime.now().isoformat()
                    }
                    papers.append(paper)
                
                # 避免请求过快
                time.sleep(1)
                
            except requests.exceptions.Timeout:
                print(f"⚠️  搜索 '{keyword}' 超时")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  搜索 '{keyword}' 失败：{e}")
            except Exception as e:
                print(f"⚠️  搜索 '{keyword}' 错误：{e}")
        
        return papers
    
    def _get_pdf_link(self, entry):
        """获取 PDF 链接"""
        if hasattr(entry, 'links'):
            for link in entry.links:
                if link.type == 'application/pdf':
                    return link.href
        return entry.links[0].href if entry.links else ''
    
    def save_papers(self, papers):
        """保存论文到本地"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = PAPERS_DIR / f"papers_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'search_date': datetime.now().isoformat(),
                'total_papers': len(papers),
                'papers': papers
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已保存 {len(papers)} 篇论文到 {filename}")
        return filename


class SemanticScholarScraper:
    """Semantic Scholar 论文抓取器（需要 API Key）"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    def search(self, query, limit=10):
        """搜索论文"""
        params = {
            'query': query,
            'limit': limit,
            'fields': 'title,authors,abstract,publicationDate,venue,citationCount,url'
        }
        
        if self.api_key:
            params['api_key'] = self.api_key
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            papers = []
            for paper in data.get('data', []):
                papers.append({
                    'title': paper.get('title', ''),
                    'authors': [a.get('name', '') for a in paper.get('authors', [])],
                    'abstract': paper.get('abstract', ''),
                    'publication_date': paper.get('publicationDate', ''),
                    'venue': paper.get('venue', ''),
                    'citation_count': paper.get('citationCount', 0),
                    'url': paper.get('url', ''),
                    'source': 'Semantic Scholar',
                    'captured_at': datetime.now().isoformat()
                })
            
            return papers
            
        except Exception as e:
            print(f"Semantic Scholar 搜索错误：{e}")
            return []


def fetch_latest_papers(keywords=None, days_back=7, max_per_keyword=5):
    """获取最新论文的主函数"""
    if keywords is None:
        keywords = DEFAULT_KEYWORDS[:5]  # 默认使用前 5 个关键词
    
    print(f"🔍 开始搜索论文，关键词：{keywords}")
    print(f"📅 时间范围：最近 {days_back} 天\n")
    
    scraper = ArXivScraper(max_results=max_per_keyword)
    papers = scraper.search(keywords, days_back)
    
    # 去重（基于标题）
    seen = set()
    unique_papers = []
    for p in papers:
        if p['title'] not in seen:
            seen.add(p['title'])
            unique_papers.append(p)
    
    print(f"\n📊 共找到 {len(unique_papers)} 篇独特论文\n")
    
    # 保存
    if unique_papers:
        scraper.save_papers(unique_papers)
    
    return unique_papers


if __name__ == "__main__":
    papers = fetch_latest_papers()
    for p in papers[:3]:
        print(f"📄 {p['title']}")
        print(f"   作者：{', '.join(p['authors'][:3])}...")
        print(f"   来源：{p['source']} | {p['published']}\n")
