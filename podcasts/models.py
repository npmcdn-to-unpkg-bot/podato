from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    """Podcast categories"""
    name = models.CharField(max_length=20, primary_key=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Podcast(models.Model):
    url = models.CharField(max_length=255, primary_key=True)
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True)
    description = models.TextField()
    image = models.CharField(max_length=255, null=True)
    explicit = models.CharField(max_length=1,default=-1, choices=[("u", "not set",),("c", "clean"), ("e", "explicit")])
    owner_email = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    tags = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    last_fetched = models.DateTimeField()

    def __str__(self):
        return self.title


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, null=False)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    summary = models.CharField(max_length=500)
    description = models.TextField()
    content = models.TextField()
    enclosure_type = models.CharField(max_length=20)
    enclosure_url = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(default=0)
    explicit = models.CharField(max_length=1, choices=[("u", "not set",),("c", "clean"), ("e", "explicit")])
    author = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    published = models.DateTimeField()

    def __str__(self):
        return self.title




