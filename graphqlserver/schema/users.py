from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from graphene import relay, ObjectType

class UserNode(DjangoNode):
    class Meta:
        model = User
        filter_fields = ['username', 'email']
        filter_order_by = ['username', "id"]
        only_fields = ("username", "email", "is_staff", "date_joined", )


class UserQuery(ObjectType):
    user = relay.NodeField(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    class Meta:
        abstract = True
