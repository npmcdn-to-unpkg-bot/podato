from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^graphiql', views.graphiql, name="graphiql"),
]