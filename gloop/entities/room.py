from gloop.entities import Entity


class Room(Entity):

    def __init__(self, _id=None, _description=None):
        self._id = _id
        self._description = _description

    def copy(self):
        return Room(
            _id=self._id,
            _description=str(self._description)
        )

    def to_dict(self) -> dict:
        return dict(
            _id=self._id,
            _description=self._description
        )
