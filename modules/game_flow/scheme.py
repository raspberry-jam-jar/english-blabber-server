# import graphene
#
# from graphene_django.types import DjangoObjectType
# from graphene_django.rest_framework.mutation import SerializerMutation
# from graphql_jwt.decorators import login_required
#
# from game_flow.models import UserGift
# from game_flow.serializers import UserGiftSerializer
#
#
# class UserGiftType(DjangoObjectType):
#     class Meta:
#         model = UserGift
#
#
# class UserGiftMutation(SerializerMutation):
#     class Arguments:
#         serializer_class = UserGiftSerializer
#
#     gift = graphene.Field(UserGiftType)
#
#     @login_required
#     def get_serializer_kwargs(cls, root, info, **input):
#         pass
#
#
# class Mutation(graphene.ObjectType):
#     buy_or_use_gift = UserGiftMutation.Field()
