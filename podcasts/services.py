from django.db import models, transaction

import datetime

from podcasts.models import Podcast
from podcasts.fetcher import fetcher

def get_podcast_by_url(url):
    """Gets a podcast given its feed url. Fetches it if it's not yet in the database."""
    try:
        podcast = Podcast.objects.get(url=url)
    except models.ObjectDoesNotExist:
        podcast = None
    if not podcast:
        podcast = fetcher.fetch(url)
        podcast = podcast.save_to_db()

    return podcast


def update_podcast(podcast):
    """Refetches the podcast corresponding to the given podcast object."""
    fetcher.fetch(podcast.url).save_to_db()


@transaction.atomic
def subscribe_user_to_podcast(user, podcast):
    """Subscribe the user to the given podcast. Returns True if successful, False if already subscribed."""
    if not is_user_subscribed(user, podcast):
        user.subscriptions.create(podcast=podcast)
        return True
    return False


def unsubscribe_user_from_podcast(user, podcast):
    """Unsubscribe the user from the given podcast."""
    return user.subscriptions.filter(podcast=podcast, unsubscribed=None)\
        .update(unsubscribed=datetime.datetime.utcnow()) > 0


def is_user_subscribed(user, podcast):
    """Returns whether the user is subscribed to the given podcast."""
    return user.subscriptions.filter(podcast=podcast, unsubscribed=None).count() > 0