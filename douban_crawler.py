import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import logging
import re
import json

logger = logging.getLogger(__name__)


class DoubanTopCrawler:
    BASE_URL = "https://movie.douban.com/top250"

    def __init__(self, count: int = 50, delay: float = 1.0):
        self.count = count
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })

    def _parse_item(self, item_el) -> dict:
        rank_text = item_el.select_one(".pic em").get_text(strip=True)
        rank = int(rank_text)

        # Only use the first <span class="title"> for the primary Chinese title
        title_span = item_el.select_one(".hd .title")
        title = title_span.get_text(strip=True) if title_span else ""
        url = item_el.select_one(".hd a")["href"]

        img_el = item_el.select_one(".pic img")
        cover_url = img_el["src"] if img_el else ""

        rating_el = item_el.select_one(".rating_num")
        rating = float(rating_el.get_text(strip=True)) if rating_el else 0.0

        # Vote count: in .bd div, the last <span> without a class contains "N人评价"
        bd_div = item_el.select_one(".bd")
        vote_text = "0"
        if bd_div:
            inner_div = bd_div.find("div", recursive=False)
            if inner_div:
                spans = inner_div.find_all("span")
                for sp in spans:
                    text = sp.get_text(strip=True)
                    if "人评价" in text:
                        vote_text = text
                        break
        vote_count = int(re.sub(r"[^\d]", "", vote_text)) if vote_text else 0

        info_el = item_el.select_one(".bd p:first-child")
        info = info_el.get_text("\n", strip=True) if info_el else ""

        quote_el = item_el.select_one(".quote .inq")
        quote = quote_el.get_text(strip=True) if quote_el else ""

        return {
            "rank": rank,
            "title": title,
            "rating": rating,
            "vote_count": vote_count,
            "info": info,
            "quote": quote,
            "url": url,
            "cover_url": cover_url,
        }

    def crawl(self) -> list[dict]:
        movies: list[dict] = []
        pages_needed = (self.count // 25) + (1 if self.count % 25 else 0)

        for page in range(pages_needed):
            start = page * 25
            url = f"{self.BASE_URL}?start={start}&filter="

            logger.info("Fetching page %d: %s", page + 1, url)
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
            except requests.RequestException as e:
                logger.warning("Failed: %s", e)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".grid_view .item")

            for item_el in items:
                movie = self._parse_item(item_el)
                if movie["rank"] <= self.count:
                    movies.append(movie)

            if len(movies) >= self.count:
                break

            time.sleep(self.delay)

        movies.sort(key=lambda m: m["rank"])
        return movies[:self.count]

    def save_json(self, movies: list[dict], filepath: str = "douban_top50.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
        logger.info("Saved to %s", filepath)