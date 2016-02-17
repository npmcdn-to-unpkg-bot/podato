from graphene import relay, Schema
from graphene.contrib.django.debug import DjangoDebugPlugin
from graphql.core.execution.middlewares.gevent import GeventExecutionMiddleware
from graphql.core.execution import Executor
from django.conf import settings
from user_nodes import UserQuery
from podcast_nodes import PodcastQuery, PodcastMutations


class Query(UserQuery, PodcastQuery):
    node = relay.NodeField()


class Mutation(PodcastMutations):
    pass

plugins = []
if settings.DEBUG:
    plugins = [DjangoDebugPlugin()]

schema = Schema(name="Podato Schema",
                executor=Executor([GeventExecutionMiddleware()]),
                plugins=plugins,
                query=Query,
                mutation=Mutation
                )
