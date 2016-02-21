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
    url = models.CharField(max_length=255, primary_key=True, help_text="The podcast's feed url.")
    link = models.CharField(max_length=255, help_text="A link to the podcast's website.")
    title = models.CharField(max_length=200, help_text="The podcast's title.")
    author = models.CharField(max_length=200, blank=True, null=True, help_text="The podcast's author.")
    description = models.TextField(help_text="The podcast's description.")
    copyright = models.CharField(max_length=200, blank=True, null=True, help_text="A podcast's copyright statement.")
    image = models.URLField(max_length=255, blank=True, null=True, help_text="The url of an image for the podcast.")
    explicit = models.CharField(max_length=1,default="u",
                                choices=[("u", "not set",),("c", "clean"), ("e", "explicit")],
                                help_text="Whether the podcast contains explicit content.")
    owner_email = models.CharField(max_length=200, blank=True, null=True, help_text="The email of the podcast's owner.")
    owner_name = models.CharField(max_length=200, blank=True, null=True, help_text="The podcast owner's name.")
    tags = SeparatedValuesField(max_length=200, blank=True, null=True, help_text="Podcast tags.")
    categories = models.ManyToManyField(Category, help_text="Tags that describe the podcast.")
    last_fetched = models.DateTimeField(help_text="When the podcast feed was last fetched.")
    warnings = SeparatedValuesField(max_length=200, blank=True, null=True, help_text="Any warnings generated while fetching.")
    language = models.CharField(max_length=20, blank=True, null=True, help_text="The language the podcast is in.")

    subscribers = models.ManyToManyField(to=User, through="Subscription", related_name="subscriptions", help_text="The users who subscribe to this podcast.")

    objects = PodcastManager()

    def __str__(self):
        return self.title


class Episode(models.Model):
    """Represents a podcast episode."""
    guid = models.CharField(max_length=400, primary_key=True, help_text="The episode's unique identifier.")
    podcast = models.ForeignKey(Podcast, null=True, related_name="episodes", help_text="The podcast this episode belongs to.")
    title = models.CharField(max_length=255, help_text="The episode title.")
    link = models.URLField(max_length=255, help_text="A web link to the episode.")
    subtitle = models.CharField(max_length=255, blank=True, null=True, help_text="The episode subtitle.")
    summary = models.CharField(max_length=500, blank=True, null=True, help_text="A summary of the episode.")
    description = models.TextField(blank=True, null=True, help_text="A description of the episode")
    content = models.TextField(blank=True, null=True, help_text="Content of the post (from RSS feed).")
    enclosure_type = models.CharField(max_length=20, help_text="The type of file this episode is.")
    enclosure_url = models.URLField(max_length=255, help_text="The url of the file for this episode.")
    duration = models.PositiveIntegerField(default=0, help_text="The duration of this episode;")
    explicit = models.CharField(max_length=1, default="u", choices=[("u", "not set",),("c", "clean"), ("e", "explicit")],
                                help_text="Whether this episode contains explicit content.")
    author = models.CharField(max_length=255, blank=True, null=True, help_text="The author of this episode.")
    image = models.URLField(max_length=255, blank=True, null=True, help_text="The image associated with this episode.")
    published = models.DateTimeField(help_text="The moment this episode was published.")
    warnings = SeparatedValuesField(max_length=200, blank=True, null=True, help_text="Any warnings generated while fetching.")

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """A subscription model represents a subscription from a user to a podcast.

    Note that a user may have multiple subscriptions for the same podcast. If a user unsubscribes from a podcast, the
    subscription isn't deleted, but rather, the unssubscribed field is set. So to get a list of all podcasts the user is
    currently subscribed to, get all subscriptions whose unsubscribed field is None."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="subscription_objs")
    podcast = models.ForeignKey(Podcast, related_name="subscriptions")
    subscribed = models.DateTimeField(auto_now_add=True, help_text="The date on which the user subscribed to this podcast")
    unsubscribed = models.DateTimeField(help_text="The date on which the user unsubscribed from this podcast.", null=True)

    def __str__(self):
        return "%s -> %s" % (self.user.username, self.podcast.title)




