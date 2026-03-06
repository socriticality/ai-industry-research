"""
笔记系统 - 存储和管理研究思考
"""
import json
from datetime import datetime
from pathlib import Path
from config.settings import NOTES_DIR


class NoteManager:
    """研究笔记管理器"""
    
    def __init__(self):
        self.notes_dir = NOTES_DIR
        self.index_file = self.notes_dir / "notes_index.json"
        self._ensure_index()
    
    def _ensure_index(self):
        """确保索引文件存在"""
        if not self.index_file.exists():
            self._save_index([])
    
    def _load_index(self):
        """加载索引"""
        with open(self.index_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_index(self, index):
        """保存索引"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def create_note(self, title, content, tags=None, related_paper=None, related_news=None):
        """创建新笔记"""
        note_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        note = {
            'id': note_id,
            'title': title,
            'content': content,
            'tags': tags or [],
            'related_paper': related_paper,
            'related_news': related_news,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'version': 1
        }
        
        # 保存笔记内容
        note_file = self.notes_dir / f"{note_id}.md"
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"*创建时间：{note['created_at']}*\n\n")
            if tags:
                f.write(f"**标签：** {', '.join(tags)}\n\n")
            f.write("---\n\n")
            f.write(content)
        
        # 更新索引
        index = self._load_index()
        index.append({
            'id': note_id,
            'title': title,
            'tags': tags or [],
            'created_at': note['created_at'],
            'file': str(note_file)
        })
        self._save_index(index)
        
        print(f"✓ 笔记已创建：{note_file}")
        return note
    
    def list_notes(self, tag_filter=None):
        """列出所有笔记"""
        index = self._load_index()
        
        if tag_filter:
            index = [n for n in index if tag_filter in n.get('tags', [])]
        
        return index
    
    def get_note(self, note_id):
        """获取笔记内容"""
        note_file = self.notes_dir / f"{note_id}.md"
        if note_file.exists():
            with open(note_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def update_note(self, note_id, new_content=None, new_tags=None):
        """更新笔记"""
        note_file = self.notes_dir / f"{note_id}.md"
        if not note_file.exists():
            print(f"✗ 笔记不存在：{note_id}")
            return None
        
        with open(note_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if new_content:
            content = content.split('---\n\n')[0] + '\n\n---\n\n' + new_content
        
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新索引中的更新时间
        index = self._load_index()
        for note in index:
            if note['id'] == note_id:
                note['updated_at'] = datetime.now().isoformat()
                if new_tags:
                    note['tags'] = new_tags
                break
        self._save_index(index)
        
        print(f"✓ 笔记已更新：{note_id}")
        return content
    
    def search_notes(self, query):
        """搜索笔记"""
        results = []
        query_lower = query.lower()
        
        for note_file in self.notes_dir.glob('*.md'):
            if note_file.name == 'notes_index.json':
                continue
            
            with open(note_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if query_lower in content.lower():
                results.append({
                    'file': str(note_file),
                    'snippet': content[:200] + '...' if len(content) > 200 else content
                })
        
        return results
    
    def get_all_content(self):
        """获取所有笔记内容（用于文章生成）"""
        all_notes = []
        for note_file in sorted(self.notes_dir.glob('*.md')):
            if note_file.name.endswith('.md'):
                with open(note_file, 'r', encoding='utf-8') as f:
                    all_notes.append({
                        'file': str(note_file),
                        'content': f.read()
                    })
        return all_notes


# 快捷函数
def quick_note(title, content, tags=None):
    """快速创建笔记"""
    manager = NoteManager()
    return manager.create_note(title, content, tags)


def list_all_notes():
    """列出所有笔记"""
    manager = NoteManager()
    return manager.list_notes()


if __name__ == "__main__":
    # 测试
    note = quick_note(
        "测试笔记",
        "这是关于 AI 与产业互联网关系的初步思考...\n\n"
        "1. 技术驱动因素\n"
        "2. 产业结构变化\n"
        "3. 商业模式创新",
        tags=['思考', '框架']
    )
    print(f"\n创建成功：{note['title']}")
