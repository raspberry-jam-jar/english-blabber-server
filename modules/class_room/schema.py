import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    my_user = graphene.Field(UserType)

    @login_required
    def resolve_my_user(self, info, **kwargs):
        return info.context.user
