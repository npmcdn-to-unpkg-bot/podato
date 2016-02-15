from mock import Mock

import datetime
import freezegun

from django.contrib.auth.models import User
from podcasts import models
from podcasts import services
from podcasts.fetcher import fetcher
from podcasts.parser import parsed_podcasts

FEED_URL = "http://example.com/feed.xml"

def get_valid_podcast_model():
    return models.Podcast(
        url=FEED_URL,
        link="http://example.com/podcast",
        title="example feed",
        author="Example Guy",
        description="A podcast about examples",
        last_fetched=datetime.datetime.now()
    )


def test_get_podcast_by_url_retrieves_model(monkeypatch):
    """Test that get_podcast_by_url returns the podcast model from the database if it exists."""
    podcast_model = get_valid_podcast_model()
    objects_get_mock = Mock(return_value=podcast_model)
    monkeypatch.setattr(models.Podcast.objects, "get", objects_get_mock)

    result = services.get_podcast_by_url(FEED_URL)

    assert result == podcast_model
    models.Podcast.objects.get.assert_called_with(url=FEED_URL)


def test_get_podcast_by_url_fetches_podcast_if_not_in_db(monkeypatch):
    """Test that get_podcast_by_url fetches the podcast if it isn't in the database"""
    # We want to force the podcast to be fetched, so Podcast.objects.get needs to raise an error.
    objects_get_mock = Mock(side_effect=models.models.ObjectDoesNotExist())
    # Set up the mock value for the fetcher to return.
    podcast_model = get_valid_podcast_model()
    parsed_podcast_mock = Mock(spec=parsed_podcasts.ParsedPodcast())
    parsed_podcast_mock.save_to_db.return_value = podcast_model
    fetch_mock = Mock(return_value=parsed_podcast_mock)
    monkeypatch.setattr(models.Podcast.objects, "get", objects_get_mock)
    monkeypatch.setattr(fetcher, "fetch", fetch_mock)

    result = services.get_podcast_by_url(FEED_URL)

    # Assert that it checks the db first,
    models.Podcast.objects.get.assert_called_with(url=FEED_URL)
    # Assert that it calls the fetcher.
    fetcher.fetch.asert_called_with(FEED_URL)
    # Assert that it calls the save_to_db of the parsed podcast.
    parsed_podcast_mock.save_to_db.assert_called_with()
    # Assert that it returns the model, as returned from save_to_db.
    assert result == podcast_model


def test_update_podcast(monkeypatch):
    """Test that update_podcast fetches the podcast and saves it."""
    # Set up the mock value for the fetcher to return.
    podcast_model = get_valid_podcast_model()
    parsed_podcast_mock = Mock(spec=parsed_podcasts.ParsedPodcast())
    parsed_podcast_mock.save_to_db.return_value = podcast_model
    fetch_mock = Mock(return_value=parsed_podcast_mock)
    monkeypatch.setattr(fetcher, "fetch", fetch_mock)

    services.update_podcast(podcast_model)

    fetcher.fetch.assert_called_with(FEED_URL)
    parsed_podcast_mock.save_to_db.assert_called_with()


def test_subscribe_user_to_podcast(transactional_db):
    """Test that subscribe_user_to_podcast creates a new subscription"""
    user = User(username="foo", password="monkey123", email="user@example.com")
    user.save()
    podcast = get_valid_podcast_model()
    podcast.save()
    now = datetime.datetime.now()

    with freezegun.freeze_time(now):
        services.subscribe_user_to_podcast(user, podcast)

        assert len(user.subscriptions.all()) == 1
        subscription_model = models.Subscription.objects.get(user=user)
        assert subscription_model.podcast == podcast
        assert subscription_model.subscribed.replace(tzinfo=None) == now

