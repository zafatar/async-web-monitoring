import pytest

from src.exceptions.crawler import CrawlTimeOutError
from src.services.crawler import Crawler


@pytest.mark.parametrize(
    "url, expected", (("https://reddit.com", 200), ("https://imdb.com", 403))
)
@pytest.mark.asyncio
async def test_crawler(url, expected):
    crawler = Crawler(url=url)
    await crawler.run()

    assert crawler.result.status_code == expected


@pytest.mark.asyncio
async def test_crawler_timeout():
    url = "https://httpstat.us/200?sleep=5000"

    crawler = Crawler(url=url, timeout=2)

    with pytest.raises(CrawlTimeOutError):
        await crawler.run()
