from django.db import models, transaction
from gevent.pool import Pool
import datetime

from podcasts.models import Podcast, Episode, Subscription
from podcasts.fetcher import fetcher
from podcasts.errors import InvalidFeed

def _fetch_podcast(url):
    """Fetches the podcast and stores it in the database.

    This should only be called if the podcast is not in the database, or if the podcast
    needs to be updated. other uses should use get_podcast_by_url.
    """
    try:
        podcast = fetcher.fetch(url)
    except InvalidFeed:
        return None
    return podcast.save_to_db()



def get_podcast_by_url(url):
    """Gets a podcast given its feed url. Fetches it if it's not yet in the database."""
    try:
        podcast = Podcast.objects.get(url=url)
    except models.ObjectDoesNotExist:
        podcast = _fetch_podcast(url)

    return podcast


def get_multi_podcasts_by_url(urls):
    podcast_dict = Podcast.objects.in_bulk(urls)

    pool = Pool(size=20)
    for url in urls:
        if url not in podcast_dict:
            def _get_missing_podcast(missing_url):
                podcast_dict[missing_url] = _fetch_podcast(missing_url)
            pool.spawn(_get_missing_podcast, url)

    pool.join(timeout=30)

    return podcast_dict



def update_podcast(podcast):
    """Refetches the podcast corresponding to the given podcast object."""
    fetcher.fetch(podcast.url).save_to_db()


@transaction.atomic
def subscribe_user_to_podcast(user, podcast):
    """Subscribe the user to the given podcast. Returns True if successful, False if already subscribed."""
    if not is_user_subscribed(user, podcast):
        user.subscription_objs.create(podcast=podcast)
        return True
    return False


def subscribe_user_by_urls(user, urls):
    subscribed_urls = [sub["podcast"] for sub in user.subscription_objs.values("podcast")]
    podcast_dict = get_multi_podcasts_by_url(urls)
    result_dict = {}
    podcasts = []
    for url, podcast in podcast_dict.iteritems():
        if not podcast:
            result_dict[url] = False
        else:
            podcasts.append(podcast)
            result_dict[url] = True

    Subscription.objects.bulk_create([Subscription(user=user, podcast=podcast) for podcast in podcasts
                                      if podcast.url not in subscribed_urls])
    return result_dict


def unsubscribe_user_from_podcast(user, podcast):
    """Unsubscribe the user from the given podcast."""
    return user.subscription_objs.filter(podcast=podcast).delete()[0] > 0


def is_user_subscribed(user, podcast):
    """Returns whether the user is subscribed to the given podcast."""
    return user.subscription_objs.filter(podcast=podcast).count() > 0


def get_subscribed_episodes(user):
    """Returns a queryset for all the episodes from podcasts the suer is subscribed to, in reverse publishing order."""
    return Episode.objects.filter(podcast__in=user.subscriptions.all()).order_by("-published")