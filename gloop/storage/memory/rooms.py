from gloop.entities.room import Room
from gloop.repositories.rooms import Rooms


class InMemoryRooms(Rooms):

    __memory__ = dict()

    def __init__(self, *rooms):
        super().__init__()
        for room in rooms:
            InMemoryRooms.__memory__[room._id] = room.copy()

    async def add(self, room: Room):
        InMemoryRooms.__memory__[room._id] = room.copy()
        return room._id

    async def get(self, _id):
        return InMemoryRooms.__memory__[_id].copy()

    async def all(self):
        return [room.copy() for room in InMemoryRooms.__memory__.values()]
