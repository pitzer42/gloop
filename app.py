import jinja2
import aiohttp
from aiohttp import web

TEAMPLATES_PATH = 'templates'
TEAMPLATE_EXTENTION = '.html'

db = [
    dict(
        _id = 'dummy',
        _description = 'dummy room',
        _size = 1
    )
]


async def get_or_404(_id):
    selected_item = None
    for item in db:
        if item['_id'] == _id:
            return item
    raise web.HTTPNotFound()


template_loader = jinja2.FileSystemLoader(searchpath=TEAMPLATES_PATH)
template_env = jinja2.Environment(loader=template_loader)


def template_for(view):
    template_name = view.__name__ + TEAMPLATE_EXTENTION
    return template_env.get_template(template_name)


def html_response(html):
    return web.Response(text=html, content_type='text/html')


def redirect(request, view):
    view_name = view.__name__
    view_url = request.app.router[view_name].url_for()
    raise web.HTTPFound(location=view_url)


async def index(request):
    template = template_for(index)
    create_view_url = request.app.router[create.__name__].canonical
    rendered = template.render(items=db, create_view_url=create_view_url)
    return html_response(rendered)


async def create(request):

    if request.method == 'GET':
        template = template_for(create)
        rendered = template.render()
        return html_response(rendered)
    
    if request.method == 'POST':
        data = await request.post()
        data = dict(data)
        db.append(data)
        return redirect(request, index)


async def details(request):
    _id = request.match_info['_id']
    selected_item = await get_or_404(_id)
    template = template_for(details)
    rendered = template.render(selected_item)
    return html_response(rendered)


async def join(request):
    _id = request.match_info['_id']
    selected_item = await get_or_404(_id)

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    if '_counter' not in selected_item:
        selected_item['_counter'] = 0
    selected_item['_counter'] += 1
    
    if selected_item['_counter'] == selected_item['_size']:
        await ws.send_str('starting room')

    async for msg in ws:
        print('client says: ' + str(msg[1]))
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

def create_route_get(path, handler):
    return web.get(path, handler, name=handler.__name__)

def create_route_post(path, handler):
    return web.post(path, handler, name=handler.__name__)


app = web.Application()

app.add_routes([
    create_route_get('/', index),
    create_route_get('/create', create),
    create_route_post('/create', create),
    create_route_get('/{_id}', details),
    create_route_get('/{_id}/join', join)
])

web.run_app(app)
