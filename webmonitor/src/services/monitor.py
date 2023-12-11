import asyncio
import time

from src.configs.logs import logging
from src.database.repositories.link_access_logs import LinkAccessLogsRepository
from src.entities.links import Link
from src.exceptions.monitor import SleepTimeLessThanCrawlTime
from src.services.crawler import Crawler
from src.services.html_processor import HTMLProcessor


logger = logging.getLogger(__name__)


class Monitor:
    def __init__(self, link: Link):
        self.link = link

    async def run(self):
        while True:
            logger.debug(
                f"URL: {self.link.url} | Access Interval: {self.link.access_interval}"
            )

            start_time = time.time()

            crawl_result = await Crawler(url=self.link.url).run()

            logger.info(f"\tResult: {crawl_result.status_code} | {crawl_result.link} ")

            # Check if the link is a regex match
            html_processor = HTMLProcessor(html=crawl_result.content)
            is_regex_match = html_processor.is_regex_match(self.link.search_regex)

            # Save the result in the database
            link_access_logs_repo = LinkAccessLogsRepository()
            link_access_logs_repo.insert(
                link_id=self.link.id,
                status_code=crawl_result.status_code,
                accessed_at=crawl_result.accessed_at,
                is_regex_match=is_regex_match,
            )

            # Sleep for the access interval
            end_time = time.time()
            total_time_taken = end_time - start_time
            if self.link.access_interval > total_time_taken:
                time_to_sleep = self.link.access_interval - total_time_taken
                logger.debug(f"Sleeping for {time_to_sleep} seconds")
                await asyncio.sleep(time_to_sleep)
            else:
                error_message = f"""
                    Access interval is less than the time it took to crawl the page
                    Access Interval: {self.link.access_interval}
                    Start Time: {start_time}
                    End Time: {end_time}
                    """
                logger.error(error_message)
                raise SleepTimeLessThanCrawlTime(message=error_message)
