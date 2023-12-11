import pytest

from unittest.mock import patch, Mock

import datetime

from src.services.crawler import CrawlResult
from src.entities.links import Link
from src.services.monitor import Monitor


@patch('src.database.repositories.link_access_logs.LinkAccessLogsRepository.insert')
@patch('src.services.crawler.Crawler.run')
@pytest.mark.parametrize('url', [
    'https://www.google.com',
])
@pytest.mark.asyncio
async def test_monitor_a_single_url(url, mock_crawler_run,
                                    mock_link_access_logs_repo_insert):
    mock_crawler_run.return_value = CrawlResult(
        status_code=200,
        link=url,
        accessed_at=datetime.now(),
        content='<html><body><h1>Test</h1></body></html>',
    )

    mock_link_access_logs_repo_insert.return_value = None

    link = Link(
        id=1,
        url=url,
        access_interval=60,
        search_regex='Test',
    )
    monitor = Monitor(link=link)
    await monitor.run()

    mock_crawler_run.assert_called_once_with(url=url)
