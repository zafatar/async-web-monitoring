import asyncio
import logging
from datetime import datetime

import aiohttp

from src.exceptions.crawler import CrawlRuntimeError, CrawlTimeOutError


logger = logging.getLogger(__name__)

MAX_TIMEOUT = 60


class CrawlResult:
    def __init__(self, link: str, content: str, status_code: int) -> None:
        self.link = link
        self.content = content
        self.status_code = status_code
        self.accessed_at = datetime.now()

    def __str__(self) -> str:
        return f"{self.link} - {self.status_code}"


class Crawler:
    http_session = None
    url = None
    timeout = MAX_TIMEOUT
    result = None

    def __init__(self, url: str = "", timeout: int = MAX_TIMEOUT) -> None:
        url = url.strip()

        if url != "" and url.startswith("http"):
            self.url = url
        else:
            raise ValueError("Link is required")

        if timeout:
            self.timeout = timeout

    async def set_session(self):
        self.http_session = aiohttp.ClientSession()
        return self

    async def close_session(self):
        await self.http_session.close()
        return self

    async def run(self) -> CrawlResult:
        """This method will make a GET call for the link and
           return the content and the status code

        Returns:
            tuple[str, int]: The content and the status code
        """
        if self.http_session is None:
            await self.set_session()

        try:
            async with self.http_session.get(
                self.url, allow_redirects=True, timeout=self.timeout
            ) as response:
                status_code = response.status
                content = await response.text()
                self.result = CrawlResult(self.url, content, status_code)
        except asyncio.TimeoutError as e:
            logger.error(f"Crawler TimeOut Error: {e} - raising CrawlTimeOutError")
            raise CrawlTimeOutError(url=self.url)
        except Exception as e:
            logger.error(f"Crawler Runtime Error: {e} - raising CrawlRuntimeError")
            raise CrawlRuntimeError(url=self.url)
        finally:
            await self.close_session()

        return self.result
