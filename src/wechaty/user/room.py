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

from ..config import log
from ..types import Sayable
from ..accessory import Accessory

if TYPE_CHECKING:
    from wechaty_puppet import (
        FileBox,
        RoomQueryFilter as PuppetRoomQueryFilter,
        RoomPayload
    )
    from .contact import Contact
    from .url_link import UrlLink
    from .mini_program import MiniProgram
    from .message import Message


# pylint: disable=R0903
class RoomQueryFilter:
    """
    python-wechaty room query filter
    """
    def transfer(self, query: str = None) -> PuppetRoomQueryFilter:
        """
        convert python-wechaty RoomQueryFilter to PuppetRoomQueryFilter
        """
        return PuppetRoomQueryFilter()

    @classmethod
    def to_query_filter(cls, query: str) -> RoomQueryFilter:
        """
        transfer str query filter to PuppetRoomQueryFilter
        """
        # TODO -> details in query filter
        return RoomQueryFilter()


class Room(Accessory, Sayable):
    """
    All wechat rooms(groups) will be encapsulated as a Room.
    """
    _pool: Dict[str, Room] = defaultdict()

    def __init__(self, room_id: str) -> None:
        """docs"""
        self.room_id = room_id
        self.payload: Optional[RoomPayload] = None

        if self.__class__ is Room:
            raise Exception('Room class can not be instanciated directly!')

        if self.puppet is None:
            raise Exception(
                'Room class can not be instanciated without a puppet!')

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

        puppet_query = query.transfer() if query is not None else None
        room_ids = await cls.get_puppet().room_search(puppet_query)

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
    async def find(
            cls,
            query: Union[str, RoomQueryFilter] = None) -> Union[None, Room]:
        """
        Try to find a room by filter: {topic: string | RegExp}. If get many,
        return the first one.
        :return:
        """
        log.info('Room find <%s>', json.dumps(query))

        room_query = None
        if isinstance(query, str):
            room_query = RoomQueryFilter.to_query_filter(query)

        rooms = await cls.find_all(room_query)

        if rooms is None or len(rooms) < 1:
            return None

        if len(rooms) > 1:
            log.warn('Room find() got more than one(%d) result', len(rooms))

        for index, room in enumerate(rooms):
            valid = await cls.get_puppet().room_validate(room.room_id)

            if valid:
                log.warn(
                    'Room find() confirm room[#%d] with id=%d '
                    'is valid result, return it.',
                    index,
                    room.room_id
                )
                return room
            else:
                log.info(
                    'Room find() confirm room[#%d] with id=%d '
                    'is INVALID result, try next',
                    index,
                    room.room_id
                )
        log.info('Room find() got %d rooms but no one is valid.', len(rooms))
        return None

    @classmethod
    def load(cls, room_id: str) -> Room:
        """
        dynamic load room instance
        """
        if room_id in cls._pool:
            room = cls._pool.get(room_id)
            if room is None:
                raise Exception('room not found')
            return room

        new_room = cls(room_id)
        cls._pool[room_id] = new_room
        return new_room

    def __str__(self):
        """
        string format for room instance
        """
        if self.payload is None:
            return self.__class__.__name__

        if self.payload.topic is None:
            return 'loading ...'

        return 'Room <%s>' % self.payload.topic

    def is_ready(self) -> bool:
        """
        check if room's payload is ready
        """
        return self.payload is not None

    async def ready(self, force_sync=False):
        """
        Please not to use `ready()` at the user land.
        """
        if self.is_ready():
           return

        if force_sync:
            await self.puppet.room_payload_dirty(self.room_id)
            await self.puppet.room_member_payload_dirty(self.room_id)

        self.payload = self.puppet.room_payload(self.room_id)

        if self.payload is None:
            raise Exception('Room Payload can"t be ready')

        member_ids = await self.puppet.room_members(self.room_id)

        contacts = [
            self.wechaty.Contact.load(member_id) for member_id in member_ids]

        for contact in contacts:
            try:
                contact.ready()
            except Exception as exception:
                log.error(
                    'Room ready() member.ready() rejection: %s', exception
                )

    async def say(
            self,
            some_thing: Union[str, Contact, FileBox, MiniProgram, UrlLink],
            *args
    ) -> Union[None, Message]:
        """
        Room Say(%s, %s)
        """
        log.info("Room say <%s, %s>", some_thing, args)

        msg_id = None

        # TODO -> if is str: logic should be viewed
        if isinstance(some_thing, FileBox):
            msg_id = await self.puppet.message_send_file(
                self.room_id, some_thing
            )
        elif isinstance(some_thing, Contact):
            msg_id = await self.puppet.message_send_contact(
                # pytype: disable=attribute-error
                self.room_id, some_thing.contact_id
            )
        elif isinstance(some_thing, UrlLink):
            msg_id = await self.puppet.message_send_url(
                # pytype: disable=attribute-error
                self.room_id, some_thing.payload
            )
        elif isinstance(some_thing, MiniProgram):
            msg_id = await self.puppet.message_send_mini_program(
                # pytype: disable=attribute-error
                self.room_id, some_thing.payload
            )
        else:
            raise Exception('arg unsupported: ' + some_thing)

        if msg_id is not None:
            msg = self.wechaty.Message.load(msg_id)
            await msg.ready()
            return msg
        return None

    """
    TODO -> sayTemplateStringsArray
    """

    """
    TODO -> Event emit : on
    """

    async def add(self, contact: Contact):
        """
        Add contact in a room
        """
        log.info('Room add <%s>', contact)

        await self.puppet.room_add(self.room_id, contact.contact_id)

    async def quit(self) -> None:
        """
        Add contact in a room
        """
        pass

    async def alias(self, member: Contact) -> Optional[str]:
        """
        get member alias in room
        """
        pass
