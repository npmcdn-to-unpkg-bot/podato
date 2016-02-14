from django.db import models

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

    return podcast


def update_podcast(podcast):
    """Refetches the podcast corresponding to the given podcast object."""
    fetcher.fetch(podcast.url)


def subscribe_user_to_podcast(user, podcast):
    user.subscriptions.create(podcast=podcast)