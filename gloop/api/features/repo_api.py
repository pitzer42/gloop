from aiohttp import web
from gloop.repositories import Repository


async def get_or_404(repo, key):
    try:
        return await repo.get(key)
    except KeyError:
        raise web.HTTPNotFound()


class RepositoryAPI:

    def __init__(self, repository: Repository, entity_factory: callable):
        self._repo = repository
        self._entity_factory = entity_factory

    async def all(self, request):
        entity_list = [entity.to_dict() for entity in await self._repo.all()]
        return web.json_response(entity_list)

    async def add(self, request):
        data = await request.post()
        entity = self._entity_factory(*data)
        entity_id = await self._repo.add(entity)
        response_json = dict(_id=entity_id)
        return web.json_response(response_json)

    async def get(self, request):
        entity_id = request.match_info['_id']
        selected_entity = await get_or_404(self._repo, entity_id)
        entity_json = selected_entity.to_dict()
        return web.json_response(entity_json)
