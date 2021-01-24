import jinja2
from aiohttp import web

TEAMPLATES_PATH = 'templates'
TEAMPLATE_EXTENTION = '.html'

db = []


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
        _id = data['_id']
        _description = data['_description']
        _size = data['_size']
        db.append((_id, _description, _size))
        return redirect(request, index)


async def details(request):
    _id = request.match_info['_id']
    room = None
    for item in db:
        if item[0] == _id:
            room = item
            break
    if room:
        return web.Response(text=str(_id))
    raise web.HTTPNotFound()


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
])

web.run_app(app)
