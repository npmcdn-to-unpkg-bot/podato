# coding=utf-8

import datetime
import os.path
from xml.etree.ElementTree import Element

from parser import parse_feed, _parse_duration, _parse_categories

def read_test_file(filename):
    test_dir = os.path.join(os.path.dirname(__file__), "test_data")
    return open(os.path.join(test_dir, filename + ".xml")).read()

def test_canvas():
    """Test with the well-formatted feed of the Canvas podcast."""
    feed = read_test_file("canvas")

    result = parse_feed(feed)

    assert result.title == "Canvas"
    assert result.link == "https://www.relay.fm/canvas"
    assert result.description == "Hosted by Federico Viticci and Fraser Speirs, Canvas is a podcast all about mobile productivity. Armed with iOS, Federico and Fraser will be walking through workflows, exploring the best apps for the iPad and iPhone and helping users solve problems. Hosted by Federico Viticci and Fraser Speirs."
    assert result.language == "en-US"
    assert result.copyright == u"Copyright © 2016 Relay FM"
    assert result.author == "Relay FM"
    assert result.tags == ["iPad", "iOS", "iPhone", "workflows", "productivity"]
    assert result.explicit == "clean"
    assert result.image == "http://relayfm.s3.amazonaws.com/uploads/broadcast/image/25/canvas_artwork.png"
    assert result.owner.name == "Relay FM"
    assert result.owner.email == "hello@relay.fm"
    assert sorted(result.categories) == sorted([["Technology"], ["Technology", "Gadgets"], ["Technology", "Software How-To"]])

    episode = result.episodes[0]
    assert episode.title == "Canvas 2: Document Providers"
    assert episode.summary == "Federico and Fraser go in-depth on the Document Picker and Document Provider system in iOS 9."
    assert episode.published == datetime.datetime(2016, 1, 22,10, 15)
    assert episode.enclosure.url == "http://www.podtrac.com/pts/redirect.mp3/traffic.libsyn.com/relaycanvas/Canvas-002-2016-01-12.mp3"
    assert episode.enclosure.length == 36043673
    assert episode.enclosure.type == "audio/mp3"
    assert episode.link == "http://relay.fm/canvas/2"
    assert episode.guid == "http://relay.fm/canvas/2"
    assert episode.author == "Federico Viticci and Fraser Speirs"
    assert episode.explicit == "clean"
    assert episode.duration == 2252
    assert "<li><a href=\"https://itunes.apple.com/us/app/dropbox/id327630330?mt=8&amp;uo=4\">Dropbox</a></li>" in episode.content
    assert episode.subtitle == "Federico and Fraser go in-depth on the Document Picker and Document Provider system in iOS 9."
    assert episode.description == "Federico and Fraser go in-depth on the Document Picker and Document Provider system in iOS 9."
    assert episode.image == "http://relayfm.s3.amazonaws.com/uploads/broadcast/image/25/canvas_artwork.png"


def test_parse_duration():
    assert _parse_duration("1337") == 1337
    assert _parse_duration("22:17") == 1337
    assert _parse_duration("3:42:17") == 13337


def test_categories():
    parent = Element("foo", attrib={"text":"parent"})
    child1 = Element("foo", attrib={"text":"child1"})
    child2 = Element("foo", attrib={"text":"child2"})
    grandchild = Element("foo", attrib={"text":"grandchild"})
    parent.append(child1)
    parent.append(child2)
    child2.append(grandchild)
    assert sorted(_parse_categories(parent)) == sorted([["parent", "child1"], ["parent", "child2", "grandchild"]])