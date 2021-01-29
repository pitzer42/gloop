import asyncio
import aiohttp
import functools

from aiohttp import web

from gloop.entities.room import Room
from gloop.storage.memory.rooms import InMemoryRooms

from gloop.api.features import background_tasks
from gloop.api.features.repo_api import RepositoryAPI
from gloop.api.features.join import JoinRoom


from gloop.channels.redis import RedisChannel

STATIC_FILES_PATH = './static'
REDIS_URI = 'redis://127.0.0.1:6379'


app = web.Application()

background_tasks.install(app)

rooms = InMemoryRooms.create(initial_load=[
    Room(
        _id='foo',
        _description='dummy room'
    ),
    Room(
        _id='bar',
        _description='dummy room'
    )
])

rooms_api = RepositoryAPI(rooms, Room)
channel_factory = functools.partial(RedisChannel, REDIS_URI)
join_room = JoinRoom(rooms, channel_factory)

app.add_routes([
    web.get('/rooms', rooms_api.all),
    web.post('/rooms/create', rooms_api.add),
    web.get('/rooms/{_id}', rooms_api.get),
    web.get('/rooms/{_id}/join', join_room.join),
    web.static('/', STATIC_FILES_PATH)
])

web.run_app(app)