from django.conf.urls import url, include, patterns
from django.conf import settings

from django.contrib import admin

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', admin.site.urls,),
    url("^graphql/", include("graphqlserver.urls", namespace="graphql")),
    url('', include('main.urls', namespace="main")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.insert(-1,
        url(r'^__debug__/', include(debug_toolbar.urls))
    )
