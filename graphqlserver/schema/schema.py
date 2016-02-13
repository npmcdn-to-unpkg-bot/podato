from graphene import relay, ObjectType, Schema
from graphene.contrib.django.debug import DjangoDebugPlugin
from graphql.core.execution.middlewares.gevent import GeventExecutionMiddleware
from graphql.core.execution import Executor
from django.conf import settings
from user_nodes import UserQuery
from podcast_nodes import PodcastQuery


class Query(UserQuery, PodcastQuery):
    node = relay.NodeField()


plugins = []
if settings.DEBUG:
    plugins = [DjangoDebugPlugin()]

schema = Schema(name="Podato Schema", executor=Executor([GeventExecutionMiddleware()]), plugins=plugins)
schema.query = Query
