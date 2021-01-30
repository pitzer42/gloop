""" Application that exposes a REST API for the following features:
        * create a room
        * list all rooms
        * get details about a specific room
        * join a room through web socket
"""

import os
import asyncio
import aiohttp
import functools

from aiohttp import web

from gloop.entities.room import Room
from gloop.storage.memory.rooms import InMemoryRooms
from gloop.storage.redis.rooms import RedisRooms

from gloop.api.features import background_tasks
from gloop.api.features.repo_api import RepositoryAPI
from gloop.api.features.join import JoinRoom

from gloop.channels.redis import RedisChannel


# ENVIRONMENT VARIABLES
REDIS_URI = os.environ.get('REDIS_URI', 'redis://127.0.0.1:6379')
STATIC_FILES_PATH = os.environ.get('STATIC_FILES_PATH', './static')


# FACTORIES
channel_factory = functools.partial(RedisChannel, REDIS_URI)


def room_factory(*args, **kwargs):
    room_channel = channel_factory(kwargs['_id'])
    return Room(room_channel, *args, **kwargs)


# ENTITIES AND REPOSITORIES
dummy_room = room_factory(_id='foo', _description='dummy room')
#rooms = InMemoryRooms(dummy_room)
rooms = RedisRooms(REDIS_URI, room_factory)


# FEATURES
app = web.Application()
background_tasks.install(app)

join_room = JoinRoom(rooms, channel_factory)
rooms_api = RepositoryAPI(rooms, room_factory)


async def client_ui(request):
    client_ui_path = os.path.join(STATIC_FILES_PATH, 'ui.html')
    return web.FileResponse(client_ui_path)

app.add_routes([
    web.get('/rooms', rooms_api.all),
    web.post('/rooms', rooms_api.add),
    web.get('/rooms/{_id}', rooms_api.get),
    web.get('/rooms/{_id}/join', join_room.join),
    web.get('/', client_ui)
])

web.run_app(app)
