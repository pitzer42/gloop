import asyncio
import aiohttp
from aiohttp import web

from entities.room import Room
from storage.memory.rooms import InMemoryRooms
from channels.redis import RedisChannel

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


async def get_or_404(repo, key):
    try:
        return await repo.get(key)
    except KeyError:
        raise web.HTTPNotFound()


async def index(request):
    room_list = [room.to_dict() for room in await rooms.all()]
    return web.json_response(room_list)


async def create(request):
    data = await request.post()
    room = Room(*data)
    rooms.add(room)
    request.match_info['_id'] = room._id
    return await details(request)


async def details(request):
    _id = request.match_info['_id']
    selected_room = await get_or_404(rooms, _id)
    room_dict = selected_room.to_dict()
    return web.json_response(room_dict)


async def join(request):
    _id = request.match_info['_id']
    selected_item = await get_or_404(rooms, _id)

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    channel = RedisChannel(_id, '')
    channel2 = RedisChannel(_id, '')
    await channel.connect()
    await channel2.connect()

    t_id = str(id(ws))

    async def listen_to_channel():
        while True:
            print('listening to redis channel ' + t_id)
            redis_msg = await channel.receive()
            await ws.send_str(redis_msg)

    task = asyncio.create_task(listen_to_channel())
    app['background_tasks'].append(task)



    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            await channel2.send(msg.data)
            print(t_id + ' msg sent')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('connection closed with exception %s' % ws.exception())
    print('connection closed')
    return ws


def create_background_task(coroutine):
    task = asyncio.create_task(coroutine)
    app['background_tasks'].append(task)
    return task

async def cancel_background_tasks(app):
    for task in app['background_tasks']:
        task.cancel()
        await task


app = web.Application()
app['background_tasks'] = []
app.on_cleanup.append(cancel_background_tasks)

app.add_routes([
    web.get('/', index),
    web.post('/create', create),
    web.get('/{_id}', details),
    web.get('/{_id}/join', join),
])

web.run_app(app)
