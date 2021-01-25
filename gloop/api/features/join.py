from gloop.repositories.rooms import Rooms
from gloop.api.features.repo_api import get_or_404
from gloop.api.features.background_tasks import create_background_task

from gloop.channels.web_socket import WebSocketChannel
from gloop.channels import relay_loop

from aiohttp import web

import asyncio


class Join:

    def __init__(self, rooms: Rooms, channel_factory: callable):
        super().__init__()
        self._rooms = rooms
        self._channel_factory = channel_factory

    async def join(self, request):
        _id = request.match_info['_id']
        selected_item = await get_or_404(self._rooms, _id)

        ws = web.WebSocketResponse()
        await ws.prepare(request)
        client_channel = WebSocketChannel(ws)

        room_channel = self._channel_factory(_id)

        coroutine = relay_loop(
            room_channel.receive,
            client_channel.send)

        create_background_task(request.app, coroutine)

        await relay_loop(
            client_channel.receive,
            room_channel.send
        )

        return ws
