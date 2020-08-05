import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required, staff_member_required

from .models import User, LearningGroup


class UserType(DjangoObjectType):
    class Meta:
        model = User


class LearningGroupType(DjangoObjectType):
    class Meta:
        model = LearningGroup


class Query(graphene.ObjectType):
    my_user = graphene.Field(UserType)
    learning_groups = graphene.List(LearningGroupType)

    @login_required
    def resolve_my_user(self, info, **kwargs):
        return info.context.user

    @login_required
    @staff_member_required
    def resolve_learning_groups(self, info, **kwargs):
        if info.context.user.is_teacher:
            return LearningGroup.objects.filter(
                users__in=(info.context.user, )
            )
        return LearningGroup.objects.all()
