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