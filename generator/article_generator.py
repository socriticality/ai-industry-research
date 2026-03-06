"""
文章生成器 - 将研究笔记整理成可发表的文章
"""
from datetime import datetime
from pathlib import Path
import json
from config.settings import ARTICLES_DIR, NOTES_DIR


class ArticleGenerator:
    """自媒体文章生成器"""
    
    def __init__(self):
        self.articles_dir = ARTICLES_DIR
    
    def generate_article(self, topic, notes_content, papers=None, news=None, style='analysis'):
        """
        生成文章
        
        Args:
            topic: 文章主题
            notes_content: 笔记内容列表
            papers: 相关论文列表
            news: 相关新闻列表
            style: 文章风格 (analysis, explanation, commentary)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 构建文章结构
        article = self._build_article_structure(topic, notes_content, papers, news, style)
        
        # 保存文章
        filename = self.articles_dir / f"{topic}_{timestamp}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(article)
        
        print(f"✓ 文章已生成：{filename}")
        return filename, article
    
    def _build_article_structure(self, topic, notes_content, papers, news, style):
        """构建文章结构"""
        lines = []
        
        # 标题
        lines.append(f"# {topic}")
        lines.append("")
        lines.append(f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # 引言
        lines.append("## 引言")
        lines.append("")
        lines.append(self._generate_intro(topic, papers, news))
        lines.append("")
        
        # 核心分析（来自笔记）
        lines.append("## 核心分析")
        lines.append("")
        for note in notes_content:
            if isinstance(note, dict) and 'content' in note:
                content = note['content']
                # 移除笔记的头部元数据
                if '---' in content:
                    content = content.split('---')[-1].strip()
                lines.append(content)
                lines.append("")
            else:
                lines.append(str(note))
                lines.append("")
        
        # 最新研究动态
        if papers:
            lines.append("---")
            lines.append("")
            lines.append("## 最新研究动态")
            lines.append("")
            for i, paper in enumerate(papers[:5], 1):
                lines.append(f"### {i}. {paper.get('title', '无标题')}")
                lines.append("")
                lines.append(f"- **作者：** {', '.join(paper.get('authors', [])[:3])}")
                lines.append(f"- **来源：** {paper.get('source', '')} | {paper.get('published', '')}")
                if paper.get('summary'):
                    summary = paper['summary'][:300] + '...' if len(paper['summary']) > 300 else paper['summary']
                    lines.append(f"- **摘要：** {summary}")
                lines.append("")
        
        # 相关新闻解读
        if news:
            lines.append("---")
            lines.append("")
            lines.append("## 相关新闻解读")
            lines.append("")
            for i, item in enumerate(news[:5], 1):
                lines.append(f"### {i}. {item.get('title', '无标题')}")
                lines.append("")
                lines.append(f"- **来源：** {item.get('source', '')}")
                lines.append(f"- **时间：** {item.get('published', '')}")
                if item.get('summary'):
                    summary = item['summary'][:200] + '...' if len(item['summary']) > 200 else item['summary']
                    lines.append(f"- **摘要：** {summary}")
                lines.append("")
                lines.append("**领域解读：** *（此处可添加你的专业分析）*")
                lines.append("")
        
        # 结论
        lines.append("---")
        lines.append("")
        lines.append("## 结论与展望")
        lines.append("")
        lines.append(self._generate_conclusion(topic))
        lines.append("")
        
        # 参考资料
        lines.append("---")
        lines.append("")
        lines.append("## 参考资料")
        lines.append("")
        if papers:
            lines.append("### 学术论文")
            for paper in papers[:5]:
                if paper.get('link'):
                    lines.append(f"- {paper.get('title', '')} - [链接]({paper['link']})")
            lines.append("")
        if news:
            lines.append("### 新闻报道")
            for item in news[:5]:
                if item.get('link'):
                    lines.append(f"- {item.get('title', '')} - [链接]({item['link']})")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_intro(self, topic, papers, news):
        """生成引言"""
        intro = f"本文围绕 **{topic}** 展开分析，结合最新学术研究和行业动态，"
        intro += "探讨 AI 与产业互联网发展的内在逻辑和未来趋势。\n\n"
        
        if papers:
            intro += f"本文参考了 {len(papers)} 篇最新学术论文，"
        if news:
            intro += f"并结合 {len(news)} 条行业动态进行解读。"
        
        return intro
    
    def _generate_conclusion(self, topic):
        """生成结论模板"""
        conclusion = f"""通过对 {topic} 的深入研究，我们可以得出以下几点认识：

1. **技术层面**：AI 技术正在从单点应用向系统性赋能转变
2. **产业层面**：传统产业数字化转型进入深水区
3. **生态层面**：平台化、生态化成为主流趋势

未来值得关注的方向：
- AI 与垂直行业的深度融合
- 数据要素的价值释放
- 产业互联网平台的演进路径

*（以上为框架性结论，建议根据具体研究内容补充完善）*"""
        return conclusion
    
    def generate_news_commentary(self, news_item, context_notes=None):
        """为单条新闻生成解读评论"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        lines = []
        lines.append(f"# 新闻解读：{news_item.get('title', '无标题')}")
        lines.append("")
        lines.append(f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        lines.append("## 新闻摘要")
        lines.append("")
        lines.append(f"- **来源：** {news_item.get('source', '')}")
        lines.append(f"- **时间：** {news_item.get('published', '')}")
        lines.append(f"- **链接：** {news_item.get('link', '')}")
        lines.append("")
        lines.append(news_item.get('summary', '无摘要'))
        lines.append("")
        
        lines.append("## 领域解读")
        lines.append("")
        lines.append("### 与 AI/产业互联网的关联")
        lines.append("")
        lines.append("*（此处分析新闻事件与 AI 技术、产业互联网发展的关联）*")
        lines.append("")
        
        lines.append("### 技术背景")
        lines.append("")
        lines.append("*（此处补充相关技术背景知识）*")
        lines.append("")
        
        lines.append("### 行业影响")
        lines.append("")
        lines.append("*（此处分析对行业的影响和启示）*")
        lines.append("")
        
        if context_notes:
            lines.append("## 相关研究笔记")
            lines.append("")
            for note in context_notes[:3]:
                lines.append(f"- {note.get('title', '')}")
            lines.append("")
        
        filename = self.articles_dir / f"commentary_{timestamp}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✓ 新闻解读已生成：{filename}")
        return filename


def quick_article(topic, notes=None, papers=None, news=None):
    """快速生成文章"""
    generator = ArticleGenerator()
    
    # 如果没有提供内容，加载最近的
    if notes is None:
        notes = _load_recent_notes()
    
    return generator.generate_article(topic, notes, papers, news)


def _load_recent_notes():
    """加载最近的笔记"""
    notes = []
    for note_file in sorted(NOTES_DIR.glob('*.md'), reverse=True)[:5]:
        with open(note_file, 'r', encoding='utf-8') as f:
            notes.append({'file': str(note_file), 'content': f.read()})
    return notes


if __name__ == "__main__":
    # 测试
    filename, _ = quick_article("AI 与产业互联网的融合发展")
    print(f"\n文章已保存到：{filename}")
