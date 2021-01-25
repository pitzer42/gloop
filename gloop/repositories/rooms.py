from gloop.repositories import Repository


class Rooms(Repository):
    
    async def add(self, room):
        raise NotImplementedError()

    async def get(self, _id):
        raise NotImplementedError()

    async def all(self):
        raise NotImplementedError()
