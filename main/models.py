from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from podcasts.models import Subscription

class Profile(models.Model):
    """Represents extra information about a user."""
    user = models.OneToOneField(User)
    profile_image = models.URLField()