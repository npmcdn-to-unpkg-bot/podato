# coding=utf-8

import datetime

from email.utils import parsedate_tz
from xml.etree import ElementTree

from dateutil import tz

from podcasts.podcast import Podcast, Episode, Enclosure, Person

ITUNES_NS = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"

def parse_feed(feed_str):
    """Parses a feed, and returns a Podcast instance"""
    podcast = Podcast()
    tree = ElementTree.fromstring(feed_str)
    channel = tree[0]

    for child in channel:
        if child.tag == "title":
            podcast.title = child.text
        elif child.tag == "link":
            podcast.link = child.text
        elif child.tag == "description":
            podcast.description = child.text
        elif child.tag == "language":
            podcast.language = child.text
        elif child.tag == "copyright":
            podcast.copyright = child.text
        elif child.tag == ITUNES_NS + "author":
            podcast.author = child.text
        elif child.tag == ITUNES_NS + "keywords":
            podcast.tags += child.text.split(", ")
        elif child.tag == ITUNES_NS + "explicit":
            podcast.explicit = child.text
        elif child.tag == ITUNES_NS + "image":
            podcast.image = child.attrib.get("href")
        elif child.tag == ITUNES_NS + "owner":
            podcast.owner = _parse_person(child)
        elif child.tag == ITUNES_NS + "category":
            podcast.categories += _parse_categories(child)
        elif child.tag == "item":
            podcast.episodes.append(_parse_item(child))

    return podcast


def _parse_item(item):
    """Parses an item from a podcast feed into an Episode instance"""
    episode = Episode()

    for child in item:
        if child.tag == "title":
            episode.title = child.text
        elif child.tag == "description":
            episode.description = child.text
        elif child.tag == "pubDate":
            episode.published = _parse_date(child.text)
        elif child.tag == "enclosure":
            episode.enclosure = _parse_enclosure(child)
        elif child.tag == "link":
            episode.link = child.text
        elif child.tag == "guid":
            episode.guid = child.text
        elif child.tag == ITUNES_NS + "author":
            episode.author = child.text
        elif child.tag == ITUNES_NS + "subtitle":
            episode.subtitle = child.text
        elif child.tag == ITUNES_NS + "summary":
            episode.summary = child.text
        elif child.tag == ITUNES_NS + "explicit":
            episode.explicit = child.text
        elif child.tag == ITUNES_NS + "duration":
            episode.duration = _parse_duration(child.text)
        elif child.tag == "{http://purl.org/rss/1.0/modules/content/}encoded":
            episode.content = child.text
        elif child.tag == ITUNES_NS + "image":
            if child.attrib.get("href"):
                episode.image = child.attrib["href"]

    return episode


def _parse_categories(element):
    """Parse an <itunes:category> element into a list of categories, where every category is the parent of the next one."""
    if not element.attrib.get("text"):
        return None
    if len(element) == 0:
        return [[element.attrib["text"]]]

    base = [element.attrib["text"]]
    result = []
    for child in element:
        result += map(lambda x: base + x, _parse_categories(child))

    return result


def _parse_person(tag):
    name = None
    email = None
    for child in tag:
        if child.tag == ITUNES_NS + "name":
            name = child.text
        elif child.tag == ITUNES_NS + "email":
            email = child.text

    return Person(name=name, email=email)


def _parse_date(txt):
    """This parses an RFC 2822 timestamp, and converts it to a datetime object in utc."""
    datetime_tuple = parsedate_tz(txt)
    if datetime_tuple[9] == 0:
        return datetime.datetime(*datetime_tuple[:6])

    tzinfo = tz.tzoffset("nonsense", datetime_tuple[9])

    return datetime.datetime(*datetime_tuple[:6],
            tzinfo=tzinfo).astimezone(tz.tzoffset("UTC", 0)).replace(tzinfo=None)


def _parse_enclosure(element):
    enclosure = Enclosure(url=element.attrib.get("url"), type=element.attrib.get("type"),
                          length=int(element.attrib.get("length", 0)))
    return enclosure

def _parse_duration(txt):
    parts = txt.split(":")
    total = 0
    # Go through parts from right to left.
    for i in xrange(len(parts)):
        total += float(parts[-(i+1)]) * 60**i
    return int(total)

