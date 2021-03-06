# coding=utf-8
"""This module contains methods for fetching podcasts from a feed URL."""
import requests
import datetime

from podcasts.errors import InvalidFeed
from podcasts.parser import parse_feed


def fetch(url):
    response = requests.get(url)
    if "<channel" not in response.text:
        raise InvalidFeed("The feed at %s is not a valid rss feed." % url)

    result = parse_feed(response.text)
    result.last_fetched = datetime.datetime.utcnow()
    result.url = url
    result.validate()
    return result