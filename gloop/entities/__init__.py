from abc import ABC


class Entity(ABC):

    def copy(self):
        raise NotImplementedError()

    def to_dict(self) -> dict:
        raise NotImplementedError()
