# AI 与产业互联网研究系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

自动化的研究辅助系统，用于追踪 AI 和产业互联网领域的最新发展，管理研究思考，生成自媒体文章。

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 📚 论文抓取 | 从 arXiv 自动获取最新相关论文 |
| 📰 新闻监控 | 抓取 AI 和产业互联网相关新闻 |
| 📝 笔记管理 | 存储和组织研究思考 |
| 📄 文章生成 | 自动整理笔记生成可发表文章 |
| 🔄 自动同步 | 定时同步代码到 GitHub |

## 🚀 快速开始

### 安装依赖

```bash
pip3 install --user feedparser requests
```

### 使用示例

```bash
# 查看系统状态
python3 main.py status

# 抓取最新论文
python3 main.py fetch-papers --keywords "AI industry" --days 7

# 抓取最新新闻
python3 main.py fetch-news --hours 24

# 创建笔记
python3 main.py note create --title "我的思考" --tags "框架，分析"

# 生成文章
python3 main.py article --topic "AI 与产业互联网的融合发展" --include-papers --include-news
```

## 📁 目录结构

```
ai-industry-research/
├── main.py              # 主程序入口
├── sync-github.sh       # GitHub 同步脚本
├── requirements.txt     # 依赖
├── config/
│   └── settings.py      # 配置文件
├── scrapers/
│   ├── paper_scraper.py # 论文抓取器
│   └── news_scraper.py  # 新闻抓取器
├── storage/
│   ├── note_manager.py  # 笔记管理
│   └── ...              # 数据存储
└── generator/
    └── article_generator.py  # 文章生成器
```

## 🔄 GitHub 自动同步

### 手动同步

```bash
./sync-github.sh "提交说明"
```

### 定时同步

编辑 crontab：
```bash
crontab -e
```

添加：
```
0 2 * * * cd /path/to/ai-industry-research && ./sync-github.sh "Nightly sync"
```

## 📝 工作流建议

1. **早晨** - 获取最新动态
2. **阅读时** - 记录思考到笔记
3. **写作时** - 生成文章草稿
4. **定期** - 同步到 GitHub 备份

## 🔧 配置

编辑 `config/settings.py` 自定义：
- 搜索关键词
- 新闻源
- 存储路径

## 📄 License

MIT License
