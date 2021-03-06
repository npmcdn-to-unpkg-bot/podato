from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from graphene import relay, ObjectType
import graphene

class UserNode(DjangoNode):
    """A GraphQL object that represents a user"""
    class Meta:
        model = User
        filter_fields = ['username', 'email']
        filter_order_by = ['username', "id"]
        only_fields = ("username", "email", "is_staff", "date_joined", "subscriptions")


class UserQuery(ObjectType):
    """A GraphQL object that forms the starting point for all user-related queries in GraphQL"""
    user = relay.NodeField(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    me = graphene.Field(UserNode, description="The current user.")

    def resolve_me(self, args, info):
        """Returns the current user."""
        return info.request_context.user

    class Meta:
        abstract = True
