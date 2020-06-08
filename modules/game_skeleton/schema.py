import graphene

from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from decorators import student_or_staff_member_required
from class_room.models import User
from game_skeleton.models import Gift


class GiftType(DjangoObjectType):
    can_buy = graphene.Boolean()

    class Meta:
        model = Gift
        fields = '__all__'

    def resolve_can_buy(self, info):
        # Returns only if the object was annotated
        return getattr(self, 'can_buy', None)


class Query(graphene.ObjectType):
    available_gifts = graphene.List(
        GiftType, token=graphene.String(required=True),
        user_id=graphene.Int(), is_group_wide=graphene.Boolean(),
    )

    @login_required
    @student_or_staff_member_required
    def resolve_available_gifts(self, info, user_id, **kwargs):
        """
        Return available gifts for the student user.

        :param info:
        :param user_id:
        :param kwargs:
        :return: gifts queryset
        """

        available_gifts_qs = \
            Gift.objects.\
            get_available(user=User.objects.get(id=user_id)).\
            order_by('price', 'name')

        filter_is_group_wide = kwargs.get('is_group_wide')
        if filter_is_group_wide is not None:
            return available_gifts_qs.filter(
                is_group_wide=filter_is_group_wide
            )

        return available_gifts_qs
