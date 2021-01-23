from aiohttp import web


db = []


def redirect(request, view):
    view_name = view.__name__
    view_url = request.app.router[view_name].url_for()
    raise web.HTTPFound(location=view_url)


async def index(request):
    return web.Response(text=str(db))


async def create_or_details(request):
    _id = request.match_info['_id']
    if _id in db:
        return await details(request)
    return await create(request)


async def create(request):
    _id = request.match_info['_id']
    db.append(_id)
    return redirect(request, index)


async def details(request):
    _id = request.match_info['_id']
    return web.Response(text=str(_id))


def create_route_get(path, handler):
    return web.get(path, handler, name=handler.__name__)


app = web.Application()
app.add_routes([
    create_route_get('/', index),
    create_route_get('/{_id}', create_or_details),
])
web.run_app(app)
