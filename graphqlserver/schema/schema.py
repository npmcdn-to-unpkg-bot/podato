from graphene import relay, ObjectType, Schema
from graphql.core.execution.middlewares.gevent import GeventExecutionMiddleware
from graphql.core.execution import Executor
from users import UserQuery

class Query(UserQuery):
    pass


schema = Schema(name="Podato Schema", executor=Executor([GeventExecutionMiddleware()]))
schema.query = Query
