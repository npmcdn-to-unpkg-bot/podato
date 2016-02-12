from fetcher import fetch

import mock
import pytest
import requests
import requests_mock

from podcasts.parser.test_parser import read_test_file
from podcasts.errors import InvalidFeed

FEED_URL = "http://example.com/podcast/feed.xml"

@pytest.fixture
def mock_requests(request):
    mocker = requests_mock.Mocker()
    mocker.start()

    def finalize():
        mocker.stop()

    request.addfinalizer(finalize)
    return mocker


def test_fetcher(mock_requests):
    """Test that the fetcher correctly fetches and parses a podcast feed."""
    mock_requests.get(FEED_URL, text=read_test_file("canvas"))

    result = fetch(FEED_URL)

    assert result.title == "Canvas"


def test_invalid_feed(mock_requests):
    """Test that the fetcher raises an error if the url does not point to a valid rss feed."""
    mock_requests.get(FEED_URL, text="<html><body><h1>Not A Feed!</h1></body></html>")

    with pytest.raises(InvalidFeed):
        fetch(FEED_URL)