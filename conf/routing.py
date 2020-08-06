import channels
import channels.auth
import channels_graphql_ws
from channels.routing import ProtocolTypeRouter
from django.urls import path

from schema import schema


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    async def on_connect(self, payload):
        """Handle WebSocket connection event."""

        self.scope["user"] = await channels.auth.get_user(self.scope)

    schema = schema


application = channels.routing.ProtocolTypeRouter(
    {
        "websocket": channels.auth.AuthMiddlewareStack(
            channels.routing.URLRouter(
                [path("ws/graphql/", MyGraphqlWsConsumer)]
            )
        )
    }
)
