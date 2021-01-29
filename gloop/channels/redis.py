import aioredis

from gloop.channels import Channel


class RedisChannel(Channel):

    def __init__(self, address: str, topic: str):
        super(RedisChannel, self).__init__()
        self._topic: str = topic
        self._address: str = address
        self._redis_input: aioredis.Redis = None
        self._redis_output: aioredis.Redis = None

    async def connect(self):
        self._redis_input = await aioredis.create_redis(self._address)
        self._redis_output = await aioredis.create_redis(self._address)

    async def send(self, message: str):
        # XADD <STREAM_NAME> * <KEY_A> <VALUE_A> <KEY_B> <VALUE_B> ...
        # XADD self._topic * message {message}
        if self._redis_output is None:
            self._redis_output = await aioredis.create_redis(self._address)
        package = dict(message=message)
        await self._redis_output.xadd(self._topic, package)

    async def receive(self) -> str:
        if self._redis_input is None:
            self._redis_input = await aioredis.create_redis(self._address)
        messages = await self._redis_input.xread([self._topic])
        message = messages[0]
        topic, message_hash, body = message
        content = list(body.values())[0]
        return content.decode()

    async def close(self):
        self._redis_input.close()
        self._redis_output.close()
        await self._redis_input.wait_closed()
        await self._redis_output.wait_closed()
