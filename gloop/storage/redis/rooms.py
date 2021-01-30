import aioredis

from gloop.entities.room import Room
from gloop.repositories.rooms import Rooms


class RedisRooms(Rooms):

    __HASH_PREFIX__ = 'rooms:'

    def __init__(self, redis_uri: str, room_factory: callable):
        super().__init__()
        self._redis_uri: str = redis_uri
        self._redis: aioredis.Redis = None
        self._room_factory = room_factory

    def _lazy_connection(func):
        async def wrapper(self, *args, **kwargs):
            if self._redis is None:
                self._redis = await aioredis.create_redis(self._redis_uri)
            await func(self, *args, **kwargs)
        return wrapper

    def key_for_id(self, _id):
        return RedisRooms.__HASH_PREFIX__ + str(_id)

    @_lazy_connection
    async def add(self, room: Room):
        key = self.key_for_id(room._id)
        room_dict = room.to_dict()
        await self._redis.hmset_dict(key, room_dict)
        await self._redis.sadd(RedisRooms.__HASH_PREFIX__, str(room._id))
        return room._id

    @_lazy_connection
    async def get(self, _id):
        key = self.key_for_id(_id)
        fields = await self._redis.hgetall(key)
        print('HGETALL')
        print(fields)
        return self._room_factory(_id=fields[b'_id'],_description=fields[b'_description'])

    @_lazy_connection
    async def all(self):
        results = []
        for key in await self._redis.smembers(RedisRooms.__HASH_PREFIX__):
            room = await self.get(str(key))
            results.append(room)
        return results
