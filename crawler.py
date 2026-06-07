import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class CrawlResult:
    url: str
    status_code: int
    title: Optional[str] = None
    links: list[str] = field(default_factory=list)
    error: Optional[str] = None


class WebCrawler:
    def __init__(
        self,
        max_workers: int = 5,
        request_timeout: int = 10,
        delay: float = 0.5,
        max_depth: int = 3,
        max_pages: int = 50,
    ):
        self.max_workers = max_workers
        self.request_timeout = request_timeout
        self.delay = delay
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited: set[str] = set()
        self.results: list[CrawlResult] = []
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; SimpleCrawler/1.0)",
        })

    def _is_same_domain(self, base_url: str, target_url: str) -> bool:
        return urlparse(base_url).netloc == urlparse(target_url).netloc

    def _normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def fetch_page(self, url: str) -> CrawlResult:
        try:
            logger.info("Fetching: %s", url)
            time.sleep(self.delay)
            response = self.session.get(url, timeout=self.request_timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else None

            links = []
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                full_url = urljoin(url, href)
                normalized = self._normalize_url(full_url)
                if self._is_same_domain(url, normalized):
                    links.append(normalized)

            return CrawlResult(
                url=url,
                status_code=response.status_code,
                title=title,
                links=links,
            )
        except requests.RequestException as e:
            logger.warning("Failed to fetch %s: %s", url, e)
            return CrawlResult(url=url, status_code=0, error=str(e))

    def crawl(self, start_url: str) -> list[CrawlResult]:
        queue: list[tuple[str, int]] = [(start_url, 0)]
        base_domain = urlparse(start_url).netloc

        while queue and len(self.visited) < self.max_pages:
            batch = []
            while queue and len(batch) < self.max_workers and len(self.visited) + len(batch) < self.max_pages:
                url, depth = queue.pop(0)
                normalized = self._normalize_url(url)
                if normalized in self.visited or depth > self.max_depth:
                    continue
                self.visited.add(normalized)
                batch.append((normalized, depth))

            if not batch:
                continue

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self.fetch_page, url): (url, depth)
                    for url, depth in batch
                }
                for future in as_completed(futures):
                    result = future.result()
                    self.results.append(result)
                    _, depth = futures[future]
                    if result.links and depth < self.max_depth:
                        for link in result.links:
                            if link not in self.visited:
                                queue.append((link, depth + 1))

        logger.info("Crawl finished. Visited %d pages.", len(self.visited))
        return self.results