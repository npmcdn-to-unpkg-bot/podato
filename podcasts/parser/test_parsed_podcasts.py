# coding=utf-8
"""Tests for the  podcasts module."""
import datetime

from podcasts.parser import parsed_podcasts as podcast_objects
from podcasts.parser.parsed_podcasts import ParsedPodcast, ParsedEpisode, Enclosure, Person
from podcasts import models

TEST_DATA={
    "url":"http://example.com",
    "title": "Title",
    "author":"Someone Else",
    "categories": [["a"], ["a", "b"]],
    "copyright": "All rights reserved",
    "description": "A perfectly valid podcast",
    "explicit": "clean",
    "language":"nl-BE",
    "image":"goo.gl/img",
    "last_fetched": datetime.datetime.now(),
    "link": "http://foo.com",
    "tags": ["a", "b"],
    "owner": Person(name="John Doe", email="jdoe@mail.com"),
    "episodes": [
        {
            "title": "Episode %s" % i,
            "subtitle": "Subtitle",
            "description": "The description here",
            "summary": "A short summary",
            "guid": "aCdEFg%s" % i,
            "link": "http://foo.com",
            "duration": 12345,
            "explicit": "clean",
            "author": "John Doe",
            "content": "<h1>HEADING!</h1>",
            "image": "img.com/cool.jpg",
            "published": datetime.datetime.now(),
            "enclosure": Enclosure(url="http://media.com/track%s.mp3" % i, type="audio/mp3", length=3333),
        }
    for i in xrange(5)
    ]
}

def create_valid_podcast():
    """Creates a valid podcast."""
    podcast = ParsedPodcast(**TEST_DATA)
    podcast.episodes = map(lambda d: ParsedEpisode(**d), podcast.episodes)
    return podcast


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


def test_duplicate_guid_removed():
    """Test that validating a podcast with two episode with the same GUID generates the appropriate warning."""
    podcast = create_valid_podcast()
    podcast.episodes[3].guid = podcast.episodes[0].guid

    podcast.validate()

    assert len(podcast.episodes) == 4


def test_save_to_db_saves_podcast(transactional_db):
    """Test that save_to_db saves all the podcast's data."""
    podcast = create_valid_podcast()
    podcast.validate()

    podcast.save_to_db()

    db_podcast = models.Podcast.objects.get(url="http://example.com")

    db_podcast.last_fetched = db_podcast.last_fetched.replace(tzinfo=None)
    for key in TEST_DATA:
        if key in ["episodes", "categories"]: # We test episodes and categories separately.
            continue
        if key == "owner":
            assert podcast.owner.email == db_podcast.owner_email
            assert podcast.owner.name == db_podcast.owner_name
            continue
        assert getattr(podcast, key) == getattr(db_podcast, key)


def test_save_to_db_saves_episodes(transactional_db):
    """Test that save_to_db saves episodes correctly."""
    podcast = create_valid_podcast()
    podcast.validate()

    podcast.save_to_db()

    assert models.Episode.objects.count() == len(TEST_DATA["episodes"])

    for i in xrange(len(TEST_DATA["episodes"])):
        episode_data = TEST_DATA["episodes"][i]
        episode_obj = podcast.episodes[i]
        episode_model = models.Episode.objects.get(guid=episode_data["guid"])
        episode_model.published = episode_model.published.replace(tzinfo=None)
        for key in episode_data:
            if key == "enclosure":
                assert episode_data["enclosure"].type == episode_model.enclosure_type
                assert episode_data["enclosure"].url == episode_model.enclosure_url
                continue
            assert getattr(episode_obj, key) == getattr(episode_model, key)


def test_disassociate_old_episodes(transactional_db):
    """Test that episodes that are no longer in the feed are disassociated from the podcast."""
    podcast = create_valid_podcast()
    podcast.validate()
    podcast_model = podcast.save_to_db()

    assert len(podcast_model.episodes.all()) == len(TEST_DATA["episodes"])

    podcast.episodes = podcast.episodes[1:]
    podcast.save_to_db()

    assert len(podcast_model.episodes.all()) == len(TEST_DATA["episodes"]) - 1
