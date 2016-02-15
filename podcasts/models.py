from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from utils.fields import SeparatedValuesField

class Category(models.Model):
    """Podcast categories"""
    name = models.CharField(max_length=40)
    parent_name = models.CharField(max_length=40, blank=True, null=True)
    visible = models.BooleanField(default=False)

    class Meta:
        unique_together = ["name", "parent_name"]

    def __str__(self):
        return self.name



class PodcastManager(models.Manager):
    """A custom manager for the Podcast model class, which ensures that it has a subscriber_count field."""
    def get_queryset(self):
        return super(PodcastManager, self).get_queryset().annotate(subscriber_count=models.Count("subscriptions"))


class Podcast(models.Model):
    """Represents a podcast"""
    url = models.CharField(max_length=255, primary_key=True)
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    copyright = models.CharField(max_length=200, blank=True, null=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    explicit = models.CharField(max_length=1,default="u", choices=[("u", "not set",),("c", "clean"), ("e", "explicit")])
    owner_email = models.CharField(max_length=200, blank=True, null=True)
    owner_name = models.CharField(max_length=200, blank=True, null=True)
    tags = SeparatedValuesField(max_length=200, blank=True, null=True)
    categories = models.ManyToManyField(Category)
    last_fetched = models.DateTimeField()
    warnings = SeparatedValuesField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)

    objects = PodcastManager()

    def __str__(self):
        return self.title


class Episode(models.Model):
    """Represents a podcast episode."""
    guid = models.CharField(max_length=400, primary_key=True)
    podcast = models.ForeignKey(Podcast, null=True, related_name="episodes")
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    enclosure_type = models.CharField(max_length=20)
    enclosure_url = models.URLField(max_length=255)
    duration = models.PositiveIntegerField(default=0)
    explicit = models.CharField(max_length=1, default="u", choices=[("u", "not set",),("c", "clean"), ("e", "explicit")])
    author = models.CharField(max_length=255, blank=True, null=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    published = models.DateTimeField()
    warnings = SeparatedValuesField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """A subscription model represents a subscription from a user to a podcast.

    Note that a user may have multiple subscriptions for the same podcast. If a user unsubscribes from a podcast, the
    subscription isn't deleted, but rather, the unssubscribed field is set. So to get a list of all podcasts the user is
    currently subscribed to, get all subscriptions whose unsubscribed field is None."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="subscriptions")
    podcast = models.OneToOneField(Podcast, related_name="subscriptions")
    subscribed = models.DateTimeField(auto_now_add=True, help_text="The date on which the user subscribed to this podcast")
    unsubscribed = models.DateTimeField(help_text="The date on which the user unsubscribed from this podcast.", null=True)




