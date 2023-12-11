import pytest
from bs4 import BeautifulSoup

from src.services.html_processor import HTMLProcessor


@pytest.fixture
def html():
    with open("tests/mock_data/reddit-home-page.html", "r") as f:
        return f.read()


def test_html_processor(html):
    """Test HTMLProcessor class"""
    html_processor = HTMLProcessor(html)

    assert type(html_processor.soup) is BeautifulSoup


def test_html_processor_is_regex_match(html):
    """Test HTMLProcessor.is_regex_match() method"""
    html_processor = HTMLProcessor(html)

    assert (
        html_processor.is_regex_match(
            r"<title[^>]*>Reddit.*?Dive\s+into\s+anything</title>"
        )
        is True
    )
    assert html_processor.is_regex_match(r"[0-9]{2,}\s+Google") is False


def test_html_processor_is_string_match(html):
    """Test HTMLProcessor.is_string_match() method"""
    html_processor = HTMLProcessor(html)

    assert html_processor.is_string_match("Reddit") is True
    assert html_processor.is_string_match("123123   Google") is False
