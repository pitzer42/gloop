import asyncio
import aiohttp

from aiohttp import web

from gloop.api.features import background_tasks
from gloop.api.features.repo_api import RepositoryAPI
from gloop.api.features.join import Join

from gloop.storage.memory.rooms import InMemoryRooms
from gloop.entities.room import Room

from gloop.channels.redis import RedisChannel

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

join_obj = Join(rooms, lambda topic: RedisChannel(topic, REDIS_URI))

app.add_routes([
    web.get('/', rooms_api.all),
    web.post('/create', rooms_api.add),
    web.get('/{_id}', rooms_api.get),
    web.get('/{_id}/join', join_obj.join),
])

web.run_app(app)
