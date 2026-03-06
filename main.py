#!/usr/bin/env python3
"""
AI 与产业互联网研究系统 - 主程序

功能：
- 自动抓取最新论文
- 抓取相关新闻
- 管理研究笔记
- 生成自媒体文章
"""
import argparse
import sys
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])

from scrapers.paper_scraper import fetch_latest_papers
from scrapers.news_scraper import fetch_latest_news
from storage.note_manager import NoteManager, quick_note, list_all_notes
from generator.article_generator import ArticleGenerator, quick_article


def cmd_fetch_papers(args):
    """抓取论文"""
    keywords = args.keywords.split(',') if args.keywords else None
    papers = fetch_latest_papers(
        keywords=keywords,
        days_back=args.days,
        max_per_keyword=args.max
    )
    print(f"\n✅ 完成！共获取 {len(papers)} 篇论文")


def cmd_fetch_news(args):
    """抓取新闻"""
    news = fetch_latest_news(hours_back=args.hours)
    print(f"\n✅ 完成！共获取 {len(news)} 条新闻")


def cmd_note(args):
    """管理笔记"""
    manager = NoteManager()
    
    if args.action == 'create':
        content = input("输入笔记内容（输入 END 结束）:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        content = '\n'.join(lines)
        
        tags = args.tags.split(',') if args.tags else None
        manager.create_note(args.title, content, tags)
    
    elif args.action == 'list':
        notes = manager.list_notes()
        print(f"\n📝 共 {len(notes)} 篇笔记:\n")
        for note in notes:
            print(f"  [{note['id']}] {note['title']}")
            print(f"     标签：{note.get('tags', [])} | {note['created_at'][:10]}")
            print()
    
    elif args.action == 'search':
        results = manager.search_notes(args.query)
        print(f"\n🔍 搜索结果:\n")
        for r in results:
            print(f"  📄 {r['file']}")
            print(f"     {r['snippet'][:100]}...\n")


def cmd_article(args):
    """生成文章"""
    generator = ArticleGenerator()
    manager = NoteManager()
    
    # 加载笔记
    notes = manager.get_all_content()
    
    # 加载最新论文
    try:
        papers = _load_latest_papers()
    except:
        papers = []
    
    # 加载最新新闻
    try:
        news = _load_latest_news()
    except:
        news = []
    
    filename, _ = generator.generate_article(
        topic=args.topic,
        notes_content=notes,
        papers=papers if args.include_papers else None,
        news=news if args.include_news else None,
        style=args.style
    )
    print(f"\n✅ 文章已生成：{filename}")


def cmd_quick_commentary(args):
    """为新闻生成解读"""
    generator = ArticleGenerator()
    manager = NoteManager()
    
    # 加载最新新闻
    news_list = _load_latest_news()
    if not news_list:
        print("❌ 没有找到新闻，请先运行 fetch-news")
        return
    
    news = news_list[0]  # 使用最新新闻
    notes = manager.get_all_content()
    
    filename = generator.generate_news_commentary(news, notes)
    print(f"\n✅ 新闻解读已生成：{filename}")


def cmd_status(args):
    """显示系统状态"""
    print("\n📊 AI 与产业互联网研究系统")
    print("=" * 50)
    
    # 统计笔记
    note_count = len(list(NoteManager().list_notes()))
    print(f"📝 研究笔记：{note_count} 篇")
    
    # 统计论文
    from config.settings import PAPERS_DIR
    paper_files = list(PAPERS_DIR.glob('*.json'))
    print(f"📚 论文数据：{len(paper_files)} 次抓取")
    
    # 统计新闻
    from config.settings import NEWS_DIR
    news_files = list(NEWS_DIR.glob('*.json'))
    print(f"📰 新闻数据：{len(news_files)} 次抓取")
    
    # 统计文章
    from config.settings import ARTICLES_DIR
    article_files = list(ARTICLES_DIR.glob('*.md'))
    print(f"📄 生成文章：{len(article_files)} 篇")
    
    print("=" * 50)


def _load_latest_papers():
    """加载最新论文数据"""
    from config.settings import PAPERS_DIR
    import json
    
    paper_files = sorted(PAPERS_DIR.glob('*.json'), reverse=True)
    if paper_files:
        with open(paper_files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('papers', [])
    return []


def _load_latest_news():
    """加载最新新闻数据"""
    from config.settings import NEWS_DIR
    import json
    
    news_files = sorted(NEWS_DIR.glob('*.json'), reverse=True)
    if news_files:
        with open(news_files[0], 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('news', [])
    return []


def main():
    parser = argparse.ArgumentParser(
        description='AI 与产业互联网研究系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s fetch-papers --keywords "AI,industry" --days 7
  %(prog)s fetch-news --hours 24
  %(prog)s note create --title "我的思考" --tags "框架，分析"
  %(prog)s note list
  %(prog)s article --topic "AI 与产业互联网融合发展" --include-papers --include-news
  %(prog)s status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # fetch-papers
    p_papers = subparsers.add_parser('fetch-papers', help='抓取最新论文')
    p_papers.add_argument('--keywords', type=str, help='关键词，逗号分隔')
    p_papers.add_argument('--days', type=int, default=7, help='最近 N 天')
    p_papers.add_argument('--max', type=int, default=5, help='每关键词最大结果数')
    p_papers.set_defaults(func=cmd_fetch_papers)
    
    # fetch-news
    p_news = subparsers.add_parser('fetch-news', help='抓取最新新闻')
    p_news.add_argument('--hours', type=int, default=24, help='最近 N 小时')
    p_news.set_defaults(func=cmd_fetch_news)
    
    # note
    p_note = subparsers.add_parser('note', help='管理笔记')
    p_note.add_argument('action', choices=['create', 'list', 'search'], help='操作')
    p_note.add_argument('--title', type=str, help='笔记标题')
    p_note.add_argument('--tags', type=str, help='标签，逗号分隔')
    p_note.add_argument('--query', type=str, help='搜索关键词')
    p_note.set_defaults(func=cmd_note)
    
    # article
    p_article = subparsers.add_parser('article', help='生成文章')
    p_article.add_argument('--topic', type=str, required=True, help='文章主题')
    p_article.add_argument('--include-papers', action='store_true', help='包含论文')
    p_article.add_argument('--include-news', action='store_true', help='包含新闻')
    p_article.add_argument('--style', type=str, default='analysis', choices=['analysis', 'explanation', 'commentary'])
    p_article.set_defaults(func=cmd_article)
    
    # commentary
    p_commentary = subparsers.add_parser('commentary', help='生成新闻解读')
    p_commentary.set_defaults(func=cmd_quick_commentary)
    
    # status
    p_status = subparsers.add_parser('status', help='显示系统状态')
    p_status.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
