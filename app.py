from aiohttp import web


db = []


async def index(request):
    return web.Response(text=str(db))


async def create(request):
    _id = request.match_info['_id']
    db.append(_id)
    index_view_name = index.__name__
    index_view_url = request.app.router[index_view_name].url_for()
    raise web.HTTPFound(location=index_view_url)


app = web.Application()
app.add_routes([
    web.get('/', index, name=index.__name__),
    web.get('/{_id}', create, name=create.__name__),
])
web.run_app(app)
