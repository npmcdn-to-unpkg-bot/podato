from graphene import relay, ObjectType, Schema

from users import UserQuery

class Query(UserQuery):
    pass


schema = Schema(name="Podato Schema")
schema.query = Query
