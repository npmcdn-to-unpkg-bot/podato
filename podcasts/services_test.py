from mock import Mock

import datetime
import freezegun
import random

from django.contrib.auth.models import User
from podcasts import models
from podcasts import services
from podcasts.fetcher import fetcher
from podcasts.parser import parsed_podcasts

FEED_URL = "http://example.com/feed.xml"


def get_valid_podcast_model(url=FEED_URL, episodes=0):
    podcast = models.Podcast(
        url=url,
        link="http://example.com/podcast",
        title="example feed",
        author="Example Guy",
        description="A podcast about examples",
        last_fetched=datetime.datetime.now()
    )
    for i in xrange(episodes):
        podcast.episodes.create(
            guid=url+"feed-%s" % i,
            podcast=podcast,
            title="e%s" %i,
            published=datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(1, 50)),
            enclosure_url=url + "file.mp3",
            enclosure_type="audio/mp3"
        )
    return podcast


def test_get_podcast_by_url_retrieves_model(monkeypatch):
    """Test that get_podcast_by_url returns the podcast model from the database if it exists."""
    podcast_model = get_valid_podcast_model()
    objects_get_mock = Mock(return_value=podcast_model)
    monkeypatch.setattr(models.Podcast.objects, "get", objects_get_mock)

    result = services.get_podcast_by_url(FEED_URL)

    assert result == podcast_model
    models.Podcast.objects.get.assert_called_with(url=FEED_URL)


def get_valid_user():
    return User(username="foo", password="monkey123", email="user@example.com")


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
    user = get_valid_user()
    user.save()
    podcast = get_valid_podcast_model()
    podcast.save()
    now = datetime.datetime.now()

    with freezegun.freeze_time(now):
        result = services.subscribe_user_to_podcast(user, podcast)

        assert result == True
        assert len(user.subscription_objs.all()) == 1
        subscription_model = models.Subscription.objects.get(user=user)
        assert subscription_model.podcast == podcast
        assert subscription_model.subscribed.replace(tzinfo=None) == now


def test_subscribe_user_to_podcast_twice(transactional_db):
    """Test that subscribe_user_to_podcast doesn't create a new subscription when the user is already subscribed."""
    user = User(username="foo", password="monkey123", email="user@example.com")
    user.save()
    podcast = get_valid_podcast_model()
    podcast.save()

    services.subscribe_user_to_podcast(user, podcast)
    result = services.subscribe_user_to_podcast(user, podcast)

    assert result == False
    assert len(user.subscription_objs.all()) == 1


def test_is_user_subscribed_with_not_subscribed_user(transactional_db):
    """Check is_user_subscribed returns False if the user is'nt subscribed."""
    user = get_valid_user()
    user.save()
    podcast = get_valid_podcast_model()
    podcast.save()

    result = services.is_user_subscribed(user, podcast)

    assert result == False


def test_is_user_subscribed_with_subscribed_user(transactional_db):
    """Check is_user_subscribed returns True if the user is subscribed."""
    user = get_valid_user()
    user.save()
    podcast = get_valid_podcast_model()
    podcast.save()
    user.subscription_objs.create(podcast=podcast)

    result = services.is_user_subscribed(user, podcast)

    assert result == True


def test_unsubscribe(transactional_db):
    """Test that the user is correctly unsubscribed"""
    user = get_valid_user()
    user.save()
    podcast = get_valid_podcast_model()
    podcast.save()
    user.subscription_objs.create(podcast=podcast)

    result = services.unsubscribe_user_from_podcast(user, podcast)

    assert result == True
    assert user.subscription_objs.filter(podcast=podcast).count() == 0


def test_unsubscribe_user_not_subscribed(transactional_db):
    """Test that the method still runs, but returns False when the user is not subscribed."""
    user = get_valid_user()
    user.save()
    podcast = get_valid_podcast_model()
    podcast.save()

    result = services.unsubscribe_user_from_podcast(user, podcast)

    assert result == False


def test_get_multi_podcasts_by_url(monkeypatch):
    """Test that get_multi_podcasts_by_url loads and returns the correct podcasts"""
    url1 = "http://example1.com/feed"
    url2 = "http://example2.com/feed"
    podcast1 = get_valid_podcast_model(url1)
    podcast2 = get_valid_podcast_model(url2)
    in_bulk_mock = Mock(return_value={
        url1: podcast1,
        url2: podcast2
    })
    monkeypatch.setattr(models.Podcast.objects, "in_bulk", in_bulk_mock)

    result = services.get_multi_podcasts_by_url([url1, url2])

    assert result == {url1: podcast1, url2: podcast2}


def test_get_multi_podcasts_by_url_missing_model(monkeypatch):
    """Test that get_multi_podcasts_by_url loads and returns the correct podcasts, fetching any missing podcasts."""
    # Set up 4 podcasts: 2 in the db, and 2 to be fetched.
    url1 = "http://example1.com/feed"
    url2 = "http://example2.com/feed"
    url3 = "http://example3.com/feed"
    url4 = "http://example4.com/feed"
    podcast1 = get_valid_podcast_model(url1)
    podcast2 = get_valid_podcast_model(url2)
    podcast3 = get_valid_podcast_model(url3)
    podcast4 = get_valid_podcast_model(url4)
    in_bulk_mock = Mock(return_value={
        url1: podcast1,
        url2: podcast2
    })
    parsed_podcast_mock_1 = Mock(spec=parsed_podcasts.ParsedPodcast())
    parsed_podcast_mock_2 = Mock(spec=parsed_podcasts.ParsedPodcast())
    parsed_podcast_mock_1.save_to_db.return_value = podcast3
    parsed_podcast_mock_2.save_to_db.return_value = podcast4
    fetch_mock = Mock(side_effect=lambda url: {url3: parsed_podcast_mock_1, url4: parsed_podcast_mock_2}[url])
    monkeypatch.setattr(fetcher, "fetch", fetch_mock)
    monkeypatch.setattr(models.Podcast.objects, "in_bulk", in_bulk_mock)

    result = services.get_multi_podcasts_by_url([url1, url2, url3, url4])

    assert result == {
        url1: podcast1,
        url2: podcast2,
        url3: podcast3,
        url4: podcast4
    }


def test_subscribe_user_by_urls(monkeypatch):
    url1 = "http://example1.com/feed"
    url2 = "http://example2.com/feed"
    podcast1 = get_valid_podcast_model(url1)
    podcast2 = get_valid_podcast_model(url2)
    get_multi_podcast_mock = Mock(return_value={
        url1: podcast1,
        url2: podcast2
    })
    user_model = get_valid_user()
    subscription_mock = Mock()
    monkeypatch.setattr(services, "get_multi_podcasts_by_url", get_multi_podcast_mock)
    monkeypatch.setattr(services, "Subscription", subscription_mock)
    monkeypatch.setattr(models,"Subscription", subscription_mock)

    services.subscribe_user_by_urls(user_model, [url1, url2])

    get_multi_podcast_mock.assert_called_with([url1, url2])
    assert subscription_mock.objects.bulk_create.call_count == 1
    subscription_mock.objects.bulk_create.assert_called_with([models.Subscription(podcast=podcast1), models.Subscription(podcast=podcast2)])


def test_subscribe_user_by_urls_already_subscribed(db):
    """Test that the user isn't subscribed twice to a podcast."""
    url = "http://example.com/feed"
    podcast = get_valid_podcast_model(url)
    podcast.save()
    user = get_valid_user()
    user.save()
    user.subscription_objs.create(podcast=podcast)

    services.subscribe_user_by_urls(user, [url])

    assert len(user.subscription_objs.all()) == 1


def test_get_subscribed_episodes(db):
    """Test that get_subscribed_episodes returns all episodes of podcasts the user is subscribed to"""
    user = get_valid_user()
    user.save()
    podcast1 = get_valid_podcast_model("http://example.com/feed1", episodes=4)
    podcast2 = get_valid_podcast_model("http://example.com/feed2", episodes=4)
    podcast1.save()
    podcast2.save()
    user.subscription_objs.create(podcast=podcast1)
    user.subscription_objs.create(podcast=podcast2)
    _published = lambda x: x.published

    result = tuple(services.get_subscribed_episodes(user))

    checks = tuple(sorted(list(podcast1.episodes.all()) + list(podcast2.episodes.all()), key=_published)[::-1])

    assert result == checks

