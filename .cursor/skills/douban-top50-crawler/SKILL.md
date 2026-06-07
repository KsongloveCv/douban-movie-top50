---
name: douban-top50-crawler
description: 爬取豆瓣电影评分排名前50的电影信息，包括电影名称、评分、排名、链接、封面等。Use when the user mentions 豆瓣、豆瓣电影、豆瓣评分、电影排名、豆瓣top50、douban、movie ranking、爬取豆瓣电影.
---

# 豆瓣评分排名 Top50 电影爬虫

## Instructions

When the user asks to crawl Douban top-rated movies, follow these steps:

1. **Ensure dependencies are installed**:

```bash
pip3 install -r requirements.txt
```

2. **Run via main.py**:

```bash
python3 main.py douban
```

Or **directly run the crawler script**:

```bash
python3 douban_crawler.py
```

3. **Default behavior**: Crawls Douban Top 250 movies and returns the top 50 by rating. Output saved to `douban_top50.json`.

4. **Custom options** (when running douban_crawler.py directly):

```bash
# Change count
python3 douban_crawler.py --count 100

# Change output path
python3 douban_crawler.py --output results.json

# Terminal only, no file save
python3 douban_crawler.py --no-save

# More retries for unstable network
python3 douban_crawler.py --retry 5
```

5. **Output format**: Each movie entry:

```json
{
  "rank": 1,
  "title": "肖申克的救赎",
  "rating": 9.7,
  "vote_count": 3292139,
  "quote": "希望让人自由。",
  "url": "https://movie.douban.com/subject/1292052/",
  "cover_url": "https://img3.doubanio.com/...",
  "info": "导演: 弗兰克·德拉邦特 ..."
}
```

6. **After crawling**: Present results as a ranked table:

| 排名 | 电影名称 | 评分 | 评价人数 | 一句话评价 |
|------|---------|------|---------|-----------|

7. **Want a web UI?**: If the user wants to view the results as a website, use the `douban-movie-website` skill to start a Flask server.

8. **Error handling**: If blocked by Douban anti-crawling, retry with `--retry 3`. If still failing, suggest checking network or trying later.

## Important Notes

- Douban has anti-crawling measures. The script includes proper headers and request delays with exponential backoff.
- Uses `requests` and `BeautifulSoup4`.

## Additional Resources

- For usage examples, see [examples.md](examples.md)