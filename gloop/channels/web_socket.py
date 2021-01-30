from aiohttp import WSMsgType
from aiohttp.web import WebSocketResponse

from gloop.channels import Channel


class WebSocketChannel(Channel):

    def __init__(self, ws: WebSocketResponse):
        super(WebSocketChannel, self).__init__()
        self._ws = ws

    async def connect(self):
        pass

    async def close(self):
        await self._ws.close()

    async def send(self, message: str):
        await self._ws.send_str(str(message))

    async def receive(self) -> str:
        txt_message = None
        while txt_message is None:
            message = await self._ws.receive()
            if message.type == WSMsgType.TEXT:
                txt_message = str(message.data)
        return txt_message
