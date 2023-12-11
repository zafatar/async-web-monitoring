import re

from bs4 import BeautifulSoup

from src.configs.logs import logging


logger = logging.getLogger(__name__)


class HTMLProcessor:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

    def _clean_html(self):
        """Clean the HTML"""
        # Remove all script and style elements
        for script in self.soup(["script", "style"]):
            script.extract()

        # Get the only text (no HTML tags)
        return self.soup.get_text()

    def is_regex_match(self, regex: str):
        """Check if the regex is a match in the HTML"""
        try:
            regex = re.compile(regex)
        except re.error:
            logger.error(f"Invalid regex: {regex}")
            return False

        return re.search(regex, self.html) is not None

    def is_string_match(self, string: str):
        """Check if the string is a match in the HTML"""
        return string in self._clean_html()
