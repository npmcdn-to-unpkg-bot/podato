from graphene import relay, ObjectType, Schema
from graphql.core.execution.middlewares.gevent import GeventExecutionMiddleware
from graphql.core.execution import Executor
from user_nodes import UserQuery
from podcast_nodes import PodcastQuery

class Query(UserQuery, PodcastQuery):
    node = relay.NodeField()


schema = Schema(name="Podato Schema", executor=Executor([GeventExecutionMiddleware()]))
schema.query = Query
