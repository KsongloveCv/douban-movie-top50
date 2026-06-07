# 🎬 Douban Movie Top 50

> 豆瓣电影评分排名 Top 50 — 爬虫 + Web 展示

一个爬取豆瓣电影 Top 250 中评分最高的 50 部电影，并通过精美的 Web 界面展示的项目。

## ✨ Features

- **智能爬虫** — 从豆瓣 Top 250 中按评分排序提取前 50 部电影
- **Web 展示** — 暗色主题的电影卡片界面，支持封面图、星级评分、排名徽章
- **数据缓存** — JSON 文件缓存机制，避免重复请求
- **API 接口** — RESTful API，可被其他应用调用
- **CLI 入口** — 终端命令行直接运行，输出格式化表格
- **Cursor Skills** — 附带两个 Agent Skill，支持 AI 助手自动调用

## 🚀 Quick Start

```bash
# 克隆仓库
git clone https://github.com/KsongloveCv/douban-movie-top50.git
cd douban-movie-top50

# 安装依赖
pip3 install -r requirements.txt

# 启动 Web 网站
python3 app.py
# 打开浏览器访问 http://127.0.0.1:5000

# 或者通过 CLI 运行
python3 main.py douban
```

## 📁 Project Structure

```
douban-movie-top50/
├── app.py                 # Flask 后端 (API + 页面路由)
├── douban_crawler.py      # 豆瓣爬虫核心模块
├── crawler.py             # 通用网页爬虫模块
├── main.py                # CLI 入口文件
├── requirements.txt       # Python 依赖
├── templates/
│   └── index.html         # 前端页面 (暗色主题卡片)
├── .cursor/skills/
│   ├── douban-top50-crawler/   # CLI 爬虫 Skill
│   │   ├── SKILL.md
│   │   └── examples.md
│   └── douban-movie-website/   # Web 网站 Skill
│       │   └── SKILL.md
├── .gitignore
└── README.md
```

## 🌐 Web Interface

启动网站后访问 `http://127.0.0.1:5000`，你将看到：

| 特性 | 说明 |
|------|------|
| 排名徽章 | Top 3 金色、Top 4-10 红色、其余灰色 |
| 星级评分 | 根据评分动态渲染星星 |
| 电影卡片 | 封面图 + 标题 + 评分 + 评价人数 + 一句话评价 |
| 统计栏 | 总数、最高评分、平均评分 |
| 刷新缓存 | 点击按钮重新从豆瓣爬取 |
| 响应式布局 | 适配手机与桌面 |

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI 页面 |
| `/api/movies` | GET | 返回 50 部电影 JSON 数据 |
| `/api/refresh` | GET | 强制重新爬取并更新缓存 |

**示例响应：**

```json
[
  {
    "rank": 1,
    "title": "肖申克的救赎",
    "rating": 9.7,
    "vote_count": 3292139,
    "quote": "希望让人自由。",
    "url": "https://movie.douban.com/subject/1292052/",
    "cover_url": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg",
    "info": "导演: 弗兰克·德拉邦特   主演: 蒂姆·罗宾斯 /...\n1994 / 美国 / 犯罪 剧情"
  }
]
```

## 💻 CLI Usage

```bash
# 默认爬取 Top 50
python3 main.py douban

# 使用爬虫脚本（更多选项）
python3 douban_crawler.py --count 100          # 获取前 100 部
python3 douban_crawler.py --output result.json # 自定义输出路径
python3 douban_crawler.py --no-save            # 仅终端显示
python3 douban_crawler.py --retry 5            # 增加重试次数
```

## 🧩 Cursor Skills

本项目包含两个 Cursor Agent Skill，AI 助手可根据用户意图自动调用：

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `douban-top50-crawler` | 豆瓣、豆瓣电影、豆瓣评分、电影排名 | CLI 爬取并输出表格 |
| `douban-movie-website` | 豆瓣网站、启动网站、电影网站 | 启动 Flask Web 服务 |

## ⚠️ Notes

- 本项目仅用于学习目的，请遵守豆瓣的使用条款
- 豆瓣有反爬机制，脚本已内置请求延迟和重试机制
- 如遇 IP 封锁，请等待一段时间后重试
- 封面图来自豆瓣 CDN，可能存在跨域访问限制

## 📄 License

MIT License