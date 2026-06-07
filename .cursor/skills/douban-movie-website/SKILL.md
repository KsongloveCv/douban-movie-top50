---
name: douban-movie-website
description: 启动豆瓣电影评分排名Top50的Web展示网站，以卡片形式展示电影封面、评分、评价人数等信息。Use when the user mentions 豆瓣网站、豆瓣电影网站、启动豆瓣网站、豆瓣web、豆瓣电影展示、movie website、电影网站、启动网站、start douban website、douban movie web app.
---

# 豆瓣电影 Top50 网站

## Instructions

When the user asks to start the Douban movie website, follow these steps:

1. **Ensure dependencies are installed**:

```bash
pip3 install -r requirements.txt
```

Dependencies include: `requests`, `beautifulsoup4`, `lxml`, `flask`.

2. **Check if the server is already running**:

```bash
lsof -i :5001 | grep LISTEN
```

If a process is found, the server is already running. Skip to step 4.

3. **Start the Flask server**:

```bash
cd 001-skill-test && python3 app.py
```

Note: `app.py` defaults to port 5000. If port 5000 is occupied, modify the port in `app.py` (last line) or start with a custom port:

```bash
python3 -c "from app import app; app.run(debug=False, port=5001)"
```

4. **Inform the user**: Tell them to open **http://127.0.0.1:5001** (or the chosen port) in their browser.

## Website Features

- **Homepage**: Dark-themed movie card grid with rank badges, cover images, star ratings, vote counts, and quotes
- **API endpoints**:
  - `/` — Web UI (HTML page)
  - `/api/movies` — JSON data for all 50 movies (cached in `douban_top50.json`)
  - `/api/refresh` — Force re-crawl from Douban and update cache
- **Rank badges**: Top 3 = gold, Top 4-10 = red, others = grey
- **Stats bar**: Total movies, max rating, average rating
- **Responsive**: Works on mobile and desktop

## Project Structure

```
001-skill-test/
├── app.py                    # Flask backend (routes + API)
├── douban_crawler.py         # Crawler module
├── templates/index.html      # Frontend page
├── douban_top50.json         # Cached movie data
├── requirements.txt          # Dependencies
└── main.py                   # CLI entry (python main.py douban)
```

## Troubleshooting

- **Port occupied**: Change port in `app.py` or use the custom port command above
- **Douban blocked**: The site has anti-crawling. Click "刷新缓存" button or call `/api/refresh` to retry
- **No data**: If `douban_top50.json` is missing, the server will auto-crawl on first `/api/movies` request
- **Images not loading**: Douban CDN may block direct image access. The frontend has fallback handling

## Related Skills

- For CLI-based crawling only (no website), use the `douban-top50-crawler` skill