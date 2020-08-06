import graphene
import graphql_jwt

import class_room.schema
import chat.schema
import game_skeleton.schema
import game_flow.scheme


class Query(class_room.schema.Query, game_skeleton.schema.Query,
            game_flow.scheme.Query, chat.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    buy_or_use_gift = game_flow.scheme.BuyOrUseUserGiftMutation.Field()
    add_skills = game_flow.scheme.AddSkillsMutation.Field()
    send_chat_message = chat.schema.SendMessageMutation.Field()


class Subscription(graphene.ObjectType):
    on_new_chat_message = chat.schema.OnNewChatMessage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)
