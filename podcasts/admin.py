from django.contrib import admin
from podcasts.models import Podcast, Episode, Category
# Register your models here.

admin.register(Category)
admin.register(Podcast)
admin.register(Episode)
