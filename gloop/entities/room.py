from gloop.channels import Channel
from gloop.entities import Entity


class Room(Entity):

    def __init__(self, channel: Channel, _id=None, _description=None):
        self._id = _id
        self._description = _description
        self.channel = channel

    def copy(self):
        return Room(
            self.channel,
            _id=self._id,
            _description=str(self._description)
        )

    def to_dict(self) -> dict:
        return dict(
            _id=self._id,
            _description=self._description
        )
