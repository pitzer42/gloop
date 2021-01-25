import aioredis

from channels import Channel


class RedisChannel(Channel):

    def __init__(self, topic: str, address: str):
        super(RedisChannel, self).__init__()
        self._topic: str = topic
        self._address: str = address
        self._redis: aioredis.Redis = None

    async def connect(self):
        self._redis = await aioredis.create_redis(self._address)

    async def send(self, message: str):
        # XADD self._topic * message {message}
        if self._redis is None:
            await self.connect()
        package = dict(message=message)
        await self._redis.xadd(self._topic, package)

    async def receive(self) -> str:
        if self._redis is None:
            await self.connect()
        messages = await self._redis.xread([self._topic])
        message = messages[0]
        topic, message_hash, body = message
        content = list(body.values())[0]
        return content.decode()

    async def close(self):
        self._redis.close()
        await self._redis.wait_closed()
