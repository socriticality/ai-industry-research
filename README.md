# AI 与产业互联网研究系统

自动化的研究辅助系统，用于追踪 AI 和产业互联网领域的最新发展，管理研究思考，生成自媒体文章。

## 功能

| 功能 | 说明 |
|------|------|
| 📚 论文抓取 | 从 arXiv 自动获取最新相关论文 |
| 📰 新闻监控 | 抓取 AI 和产业互联网相关新闻 |
| 📝 笔记管理 | 存储和组织研究思考 |
| 📄 文章生成 | 自动整理笔记生成可发表文章 |
| 🔍 智能关联 | 将新闻与领域知识关联解读 |

## 快速开始

### 1. 安装依赖

```bash
cd ai-industry-research
pip install -r requirements.txt
```

### 2. 使用示例

```bash
# 查看系统状态
python main.py status

# 抓取最新论文（最近 7 天）
python main.py fetch-papers --keywords "AI industry,internet" --days 7

# 抓取最新新闻（最近 24 小时）
python main.py fetch-news --hours 24

# 创建研究笔记
python main.py note create --title "我的思考" --tags "框架，分析"

# 查看所有笔记
python main.py note list

# 生成文章
python main.py article --topic "AI 与产业互联网的融合发展" --include-papers --include-news

# 为最新新闻生成解读
python main.py commentary
```

## 目录结构

```
ai-industry-research/
├── main.py              # 主程序入口
├── requirements.txt     # 依赖
├── config/
│   └── settings.py      # 配置文件
├── scrapers/
│   ├── paper_scraper.py # 论文抓取器
│   └── news_scraper.py  # 新闻抓取器
├── storage/
│   ├── note_manager.py  # 笔记管理
│   └── papers/          # 论文数据存储
│   └── notes/           # 笔记存储
│   └── news/            # 新闻数据存储
│   └── articles/        # 生成的文章
└── generator/
    └── article_generator.py  # 文章生成器
```

## 工作流建议

### 日常研究流程

1. **早晨** - 获取最新动态
   ```bash
   python main.py fetch-papers --days 1
   python main.py fetch-news --hours 24
   ```

2. **阅读时** - 记录思考
   ```bash
   python main.py note create --title "XX 论文的启发" --tags "论文，洞察"
   ```

3. **写作时** - 生成文章草稿
   ```bash
   python main.py article --topic "你的主题" --include-papers --include-news
   ```

### 定时任务（可选）

可以设置 cron 定时抓取：

```bash
# 每天早上 8 点抓取论文和新闻
0 8 * * * cd /path/to/ai-industry-research && python main.py fetch-papers --days 1
0 8 * * * cd /path/to/ai-industry-research && python main.py fetch-news --hours 24
```

## 配置

编辑 `config/settings.py` 可以自定义：

- 搜索关键词
- 新闻源
- 存储路径
- 输出格式

## 扩展

### 添加新的数据源

在 `scrapers/` 目录下创建新的抓取器，遵循现有模式。

### 集成 AI 模型

系统预留了 AI 模型接口，可以集成：
- 论文摘要自动生成
- 笔记内容智能整理
- 文章润色和优化

## 注意事项

1. arXiv API 有请求频率限制，建议设置合理的抓取间隔
2. 部分新闻源可能需要处理反爬机制
3. 生成的文章需要人工审核和编辑后再发布

## License

MIT
