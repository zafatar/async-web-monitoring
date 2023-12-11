class CrawlerException(Exception):
    """Base class for exceptions in this module."""

    pass


class CrawlRuntimeError(CrawlerException):
    """Raised when there is a runtime error."""

    message = "Crawler Runtime Generic Error: {url}"

    def __init__(self, url: str) -> None:
        super().__init__(self.message.format(url=url))


class CrawlTimeOutError(CrawlerException):
    """Raised when there is a timeout error."""

    message = "Crawler TimeOut Error: {url} - Timeout: {timeout} seconds"

    def __init__(self, url: str, timeout: int = 0) -> None:
        super().__init__(self.message.format(url=url, timeout=timeout))
