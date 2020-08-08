import channels_graphql_ws
import graphene
from graphene_django.types import DjangoObjectType

from chat.models import Message


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class OnNewChatMessage(channels_graphql_ws.Subscription):
    message = graphene.Field(MessageType)

    class Arguments:
        chatroom_id = graphene.String(required=True)

    @staticmethod
    def subscribe(root, info, chatroom_id):
        return (chatroom_id, )

    @staticmethod
    def publish(message, info, chatroom_id=None):
        assert chatroom_id is None or chatroom_id == str(message.chatroom_id)

        return OnNewChatMessage(message=message)

    @classmethod
    def new_chat_message(cls, chatroom_id, message):
        cls.broadcast(
            group=chatroom_id,
            payload=message,
        )


class Query(graphene.ObjectType):
    chatroom_history = graphene.List(MessageType,
                                     chatroom_id=graphene.String(
                                         required=True
                                     ),
                                     batch_size=graphene.Int(),
                                     datetime_cursor=graphene.String())

    def resolve_chatroom_history(self, _, chatroom_id, **kwargs):
        messages_qs =\
            Message.objects.\
            filter(chatroom_id=chatroom_id).\
            order_by('datetime_created')

        if kwargs.get('datetime_cursor'):
            messages_qs = \
                messages_qs.\
                filter(datetime_created__lt=kwargs['datetime_cursor'])

        if kwargs.get('batch_size'):
            crop_index = messages_qs.count() - kwargs['batch_size']
            if crop_index > 0:
                messages_qs = messages_qs[crop_index:]

        return messages_qs


class SendMessageMutation(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        chatroom_id = graphene.String(required=True)
        text = graphene.String(required=True)
        author_id = graphene.Int(required=True)

    def mutate(self, _, chatroom_id, text, author_id):
        message = Message.objects.create(chatroom_id=chatroom_id, text=text,
                                         author_id=author_id)

        OnNewChatMessage.new_chat_message(chatroom_id=chatroom_id,
                                          message=message)
