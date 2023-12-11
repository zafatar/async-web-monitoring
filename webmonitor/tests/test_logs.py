"""Tests for the logs module""" ""
from src.configs.logs import LOG_DATE_FORMAT


def test_log_date_format():
    """Simple test to check the date format of the logs"""
    assert LOG_DATE_FORMAT == "%Y-%m-%dT%H:%M:%S%z"
