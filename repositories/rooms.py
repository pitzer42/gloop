from abc import ABC


class Rooms(ABC):
    
    async def add(self, room):
        raise NotImplementedError()

    async def get(self, _id):
        raise NotImplementedError()

    async def all(self):
        raise NotImplementedError()
