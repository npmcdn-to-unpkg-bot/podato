from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from graphene.contrib.django.views import GraphQLView

from . import views
from .schema import schema

urlpatterns = [
    url(r'^graphiql', include('django_graphiql.urls'), name="graphiql"),
    url(r'^$', csrf_exempt(GraphQLView.as_view(schema=schema)), name="graphql")
]