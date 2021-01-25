from abc import ABC
from typing import List


class Repository(ABC):
    
    async def add(self, item) -> int:
        raise NotImplementedError()

    async def get(self, item_id):
        raise NotImplementedError()

    async def all(self) -> List:
        raise NotImplementedError()
