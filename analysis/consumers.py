from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    """Websocket consumer used for sending real time data."""
    room_code: str
    user_group_name: str

    commands = {
        'echo': 'echo',
    }

    async def connect(self):
        # do not allow unauthorized users
        if not (current_user := self.scope.get('user')) or current_user.is_anonymous:
            return

        await self.accept()

        self.user_group_name = f"user"  # TODO: parameterize this

        # create group with single user
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        # send greeting to user after accepting incoming socket (example - remove later)
        await self.channel_layer.group_send(
            group=self.user_group_name,
            message={"type": "echo", "payload": "Hello from websocket world!"}
        )

    async def receive_json(self, content, **kwargs):
        command = content.get('type')

        if settings.DEBUG:
            print("WS RECEIVE", content)

        try:
            await self.channel_layer.group_send(
                group=self.user_group_name,
                message={'type': self.commands[command]}
            )
        except KeyError:
            print(f"WS INVALID COMMAND: {command}")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            group=self.user_group_name,
            channel=self.channel_name
        )

    async def echo(self, event):
        message = event.get("payload")
        await self.send_json({"type": "echo", "payload": message})
