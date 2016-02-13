from django.contrib import admin
from podcasts.models import Podcast, Episode, Category
# Register your models here.

admin.site.register(Category)
admin.site.register(Podcast)
admin.site.register(Episode)
