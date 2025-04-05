from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room = self.scope['url_route']['kwargs'].get('room')
        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(self.room, {'type': 'chat_message', 'msg': content})

    async def chat_message(self, event):
        msg = event['msg']
        await self.send_json(content=msg)