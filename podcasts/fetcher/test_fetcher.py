from fetcher import fetch

import datetime
import pytest
import freezegun

from podcasts.parser.test_parser import read_test_file
from podcasts.errors import InvalidFeed

FEED_URL = "http://example.com/podcast/feed.xml"


def test_fetcher_returns_parsed_feed(mock_requests):
    """Test that the fetcher correctly fetches and parses a podcast feed."""
    mock_requests.get(FEED_URL, text=read_test_file("canvas"))

    result = fetch(FEED_URL)

    assert result.title == "Canvas"


def test_fetcher_sets_url(mock_requests):
    mock_requests.get(FEED_URL, text=read_test_file("canvas"))

    result = fetch(FEED_URL)

    assert result.url == FEED_URL


def test_fetcher_sets_last_fetched(mock_requests):
    mock_requests.get(FEED_URL, text=read_test_file("canvas"))

    now = datetime.datetime.now()
    with freezegun.freeze_time(now):
        result = fetch(FEED_URL)

        assert result.last_fetched == now


def test_invalid_feed(mock_requests):
    """Test that the fetcher raises an error if the url does not point to a valid rss feed."""
    mock_requests.get(FEED_URL, text="<html><body><h1>Not A Feed!</h1></body></html>")

    with pytest.raises(InvalidFeed):
        fetch(FEED_URL)