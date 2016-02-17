from django.contrib import admin
import gevent.pool
import gevent


from podcasts.models import Podcast, Episode, Category, Subscription
from podcasts.services import update_podcast



def update_podcasts(modeladmin, request, queryset):
    """An admin action to update podcasts"""
    group = gevent.pool.Group()
    for podcast in queryset:
        task = gevent.spawn(update_podcast, podcast)
        group.add(task)

    group.join()

update_podcasts.short_description = "Update selected podcast"


class PodcastAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "last_fetched"]
    actions = [update_podcasts]

admin.site.register(Category)
admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Episode)
admin.site.register(Subscription)
