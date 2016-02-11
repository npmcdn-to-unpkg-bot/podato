from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from graphene import relay, ObjectType

class UserNode(DjangoNode):
    class Meta:
        model = User
        filter_fields = ['username', 'email']
        filter_order_by = ['username', "id"]

    @classmethod
    def get_node(cls, id, info=None):
        raise ValueError("called with id: %s" % id)
        try:
            instance = cls._meta.model.objects.get(id=id)
            return cls(instance)
        except cls._meta.model.DoesNotExist:
            return None


class UserQuery(ObjectType):
    user = relay.NodeField(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    class Meta:
        abstract = True
