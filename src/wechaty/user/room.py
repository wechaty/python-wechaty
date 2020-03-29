"""
python-implementation for room
"""
from __future__ import annotations
from collections import defaultdict
# from threading import Event, Thread

from typing import (
    Dict,
    List,
    Optional,
    Union,
    TYPE_CHECKING
)
import json
import logging
from ..types import Sayable
from ..accessory import Accessory

if TYPE_CHECKING:
    from wechaty_puppet import (
        FileBox,
        RoomQueryFilter
    )
    from .contact import Contact
    from .url_link import UrlLink
    from .mini_program import MiniProgram
    from .message import Message

log = logging.getLogger('Room')


class Room(Accessory, Sayable):
    """
    All wechat rooms(groups) will be encapsulated as a Room.
    """
    _pool: Dict[str, Room] = defaultdict()

    def __init__(self, room_id: str) -> None:
        """docs"""
        self.room_id = room_id

    async def say(
            self,
            text: str,
            reply_to: Union[
                str,
                Contact,
                List[Contact],
                FileBox,
                UrlLink,
                MiniProgram]) -> Optional[Message]:
        """
        """
        pass

    @classmethod
    async def create(
            cls,
            contacts: List[Contact],
            topic: str = None) -> Room:
        """
        create room instance
        """
        if not hasattr(contacts, "__len__"):
            raise Exception('contacts should be list type')
        if len(contacts) < 2:
            raise Exception('contactList need at least 2 contact to create a new room')

        log.info(
            "Room create <%s, %s>",
            ",".join([contact.contact_id for contact in contacts]),
            topic
        )

        try:
            contact_ids = list(map(lambda x: x.contact_id, contacts))
            room_id = await cls.get_puppet().room_create(contact_ids, topic)
            return cls.load(room_id)
        except Exception as exception:
            log.error(
                "Room create error <%s>",
                str(exception.args)
            )
            raise Exception("Room create error")

    @classmethod
    async def find_all(cls, query: RoomQueryFilter = None) -> List[Room]:
        """
        find room by query filter
        :param query:
        :return:
        """
        log.info('Room find_all <%s>', json.dumps(query))

        room_ids = await cls.get_puppet().room_search(query)
        rooms = [cls.load(room_id) for room_id in room_ids]

        room_result = []
        # TODO -> chang to more efficient way
        # jointly run async ready method
        for room in rooms:
            try:
                await room.ready()
                room_result.append(room)
            except Exception as exception:
                log.warn(
                    'Room findAll() room.ready() rejection: %s',
                    exception.args
                )
        return room_result

    @classmethod
    def load(cls, room_id: str) -> Room:
        """
        doc
        """
        return Room(room_id)

    async def ready(self):
        """

        :return:
        """
        pass

    async def quit(self) -> None:
        """docs"""
        pass

    async def alias(self, member: Contact) -> Optional[str]:
        """
        get member alias in room
        """
        pass
