from crawler import WebCrawler
from douban_crawler import DoubanTopCrawler


def crawl_generic():
    crawler = WebCrawler(max_depth=2, max_pages=20, delay=0.5)
    target_url = "https://example.com"

    print(f"Starting crawl: {target_url}")
    print(f"Config: max_depth={crawler.max_depth}, max_pages={crawler.max_pages}, delay={crawler.delay}s")
    print("-" * 50)

    results = crawler.crawl(target_url)

    print("-" * 50)
    print(f"\nCrawl complete!")
    print(f"  Pages visited: {len(results)}")

    for page in results:
        print(f"\n  [{page.status_code}] {page.url}")
        if page.title:
            print(f"      Title: {page.title}")
        print(f"      Links found: {len(page.links)}")


def crawl_douban_top50():
    crawler = DoubanTopCrawler(count=50)
    print("正在爬取豆瓣评分排名前50的电影...")
    print("=" * 70)

    movies = crawler.crawl()

    if not movies:
        print("爬取失败，请检查网络连接或豆瓣反爬限制。")
        return

    print(f"\n豆瓣评分排名前{len(movies)}部电影：")
    print("-" * 70)
    print(f"{'排名':<6}{'电影名':<30}{'评分':<8}{'评价人数':<12}{'链接'}")
    print("-" * 70)

    for movie in movies:
        print(f"{movie['rank']:<6}{movie['title']:<30}{movie['rating']:<8}{movie['vote_count']:<12}{movie['url']}")

    print("-" * 70)
    print(f"\n爬取完成！共获取 {len(movies)} 部电影信息。")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "douban":
        crawl_douban_top50()
    else:
        crawl_generic()