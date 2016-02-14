# coding=utf-8
"""Tests for the  podcasts module."""
import datetime

from podcasts.parser import parsed_podcasts as podcast_objects
from podcasts.parser.parsed_podcasts import ParsedPodcast, ParsedEpisode, Enclosure, Person


def create_valid_podcast():
    """Creates a valid podcast."""
    return ParsedPodcast(
        title="Title",
        author="Someone Else",
        categories=[["a"], ["a", "b"]],
        copyright="All rights reserved",
        description="A perfectly valid podcast",
        explicit="clean",
        language="nl-BE",
        image="goo.gl/img",
        last_fetched=datetime.datetime.now(),
        url="http://foo.com/feed.xml",
        link="http://foo.com",
        tags=["a", "b"],
        owner=Person(name="John Doe", email="jdoe@mail.com"),
        episodes=[
            ParsedEpisode(
                title="Episode %s" % i,
                subtitle="Subtitle",
                description="The description here",
                summary="A short summary",
                guid="aCdEFg%s" % i,
                link="http://foo.com",
                duration=12345,
                explicit="clean",
                author="John Doe",
                content="<h1>HEADING!</h1>",
                image="img.com/cool.jpg",
                published=datetime.datetime.now(),
                enclosure=Enclosure(url="http://media.com/track%s.mp3" % i, type="audio/mp3", length=3333)
            )
            for i in xrange(5)
        ]
    )


def test_valid_podcast():
    """Test that a valid podcast doesn't have any warnings"""
    podcast = create_valid_podcast()

    podcast.validate()

    assert podcast.warnings == []


def test_no_author():
    """Test that validating a podcast with no author generates the appropriate warning"""
    podcast = create_valid_podcast()
    podcast.author = None

    podcast.validate()

    assert podcast.warnings[0] == podcast_objects.W_NO_AUTHOR


def test_no_description():
    """Test that validating a podcast with no description generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.description = None

    podcast.validate()

    assert podcast.warnings[0] == podcast_objects.W_NO_DESCRIPTION


def test_no_image():
    """Test that validating a podcast with no image generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.image = None

    podcast.validate()

    assert podcast.warnings[0] == podcast_objects.W_NO_IMAGE


def test_no_categories():
    """Test that validating a podcast with no categories generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.categories = None

    podcast.validate()

    assert podcast.warnings[0] == podcast_objects.W_NO_CATEGORIES


def test_no_language():
    """Test that validating a podcast with no language generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.language = None

    podcast.validate()

    assert podcast.warnings[0] == podcast_objects.W_NO_LANGUAGE


def test_no_episode_guid():
    """Test that validating a podcast with an episode with no GUID generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.episodes[0].guid = None

    podcast.validate()

    assert podcast.episodes[0].warnings[0] == podcast_objects.W_NO_GUID


def test_no_episode_duration():
    """Test that validating a podcast with an episode with no duration generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.episodes[0].duration = None

    podcast.validate()

    assert podcast.episodes[0].warnings[0] == podcast_objects.W_NO_DURATION


def test_episode_no_author():
    """Test that validating a podcast with an episode with no author generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.episodes[0].author = None

    podcast.validate()

    assert podcast.episodes[0].warnings[0] == podcast_objects.W_NO_EPISODE_AUTHOR


def test_duplicate_guid():
    """Test that validating a podcast with two episode with the same GUID generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.episodes[3].guid = podcast.episodes[0].guid

    podcast.validate()

    assert podcast.episodes[0].warnings[0] == podcast_objects.W_DUPLICATE_GUID
