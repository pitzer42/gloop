from entities.room import Room
from repositories.rooms import Rooms


class InMemoryRooms(Rooms):

    __memory__ = dict()

    @staticmethod
    def create(initial_load=[]):
        for item in initial_load:
            __memory__[item._id] = item.copy()
        return InMemoryRooms()

    async def add(self, room: Room):
        __memory__[room._id] = room.copy()

    async def get(self, _id):
        return __memory__[_id].copy()

    async def all(self):
        return [room.copy() for room in __memory__.values()]
