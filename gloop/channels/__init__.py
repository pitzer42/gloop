from abc import ABC


async def relay_loop(receive, send):
    while True:
        msg = await receive()
        await send(msg)


class Channel(ABC):

    async def __aenter__(self):
        await self.connect()
        return self

    async def connect(self):
        raise NotImplementedError()

    async def send(self, message: str):
        raise NotImplementedError()

    async def receive(self) -> str:
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        raise NotImplementedError()
