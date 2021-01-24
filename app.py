import aiohttp
from aiohttp import web


db = [
    dict(
        _id='foo',
        _description='dummy room'
    ),
    dict(
        _id='bar',
        _description='dummy room'
    )
]


async def featch_or_fail(_id):
    for item in db:
        if item['_id'] == _id:
            return item
    raise web.HTTPNotFound()


async def index(request):
    return web.json_response(db)


async def create(request):
    data = await request.post()
    data = dict(data)
    db.append(data)
    request.match_info['_id'] = data['_id']
    return await details(request)


async def details(request):
    _id = request.match_info['_id']
    selected_item = await featch_or_fail(_id)
    return web.json_response(selected_item)


async def join(request):
    _id = request.match_info['_id']
    selected_item = await featch_or_fail(_id)

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    if _id not in request.app:
        request.app[_id] = []

    request.app[_id].append(ws)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == '<close>':
                await ws.close()
            else:
                for client in request.app[_id]:
                    if client != ws:
                        await client.send_str(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocket connection closed')
    return ws


app = web.Application()

app.add_routes([
    web.get('/', index),
    web.post('/create', create),
    web.get('/{_id}', details),
    web.get('/{_id}/join', join),
])

web.run_app(app)
