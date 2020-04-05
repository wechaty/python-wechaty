"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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
from ..types import Sayable
from ..accessory import Accessory
from ..log import WechatyLogger

if TYPE_CHECKING:
    from wechaty_puppet import (
        FileBox,
        RoomQueryFilter,
        RoomPayload,
        RoomMemberQueryFilter
    )
    from .contact import Contact
    from .url_link import UrlLink
    from .mini_program import MiniProgram
    from .message import Message

log = WechatyLogger('Room')


def _build_room_query(query: Union[str, RoomQueryFilter] = None) -> RoomQueryFilter:
    """
    transfer user custom query data to RoomQueryFilter data
    """
    if isinstance(query, RoomQueryFilter):
        return query
    return RoomQueryFilter(query)


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
    async def find_all(
            cls,
            query: Union[str, RoomQueryFilter] = None) -> List[Room]:
        """
        find room by query filter
        :param query:
        :return:
        """
        log.info('Room find_all <%s>', json.dumps(query))
        room_query = _build_room_query(query)
        room_ids = await cls.get_puppet().room_search(room_query)

        rooms = [cls.load(room_id) for room_id in room_ids]

        room_result = []
        # TODO -> chang to more efficient way
        # jointly run async ready method
        for room in rooms:
            try:
                await room.ready()
                room_result.append(room)
            except Exception as exception:
                log.warning(
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

        rooms = await cls.find_all(query)

        if rooms is None or len(rooms) < 1:
            return None

        if len(rooms) > 1:
            log.warning('Room find() got more than one(%d) result', len(rooms))

        for index, room in enumerate(rooms):
            valid = await cls.get_puppet().room_validate(room.room_id)

            if valid:
                log.warning(
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

    # async def on(self, event: str, listener: Callable):

    async def add(self, contact: Contact):
        """
        Add contact in a room
        """
        log.info('Room add <%s>', contact)

        await self.puppet.room_add(self.room_id, contact.contact_id)

    async def delete(self, contact: Contact):
        """
        delete room
        """
        log.info('Room delete<%s>', contact)

        if contact is None or contact.contact_id is None:
            raise Exception('Contact is none or contact_id not found')
        await self.puppet.room_delete(self.room_id, contact.contact_id)

    async def quit(self):
        """
        Add contact in a room
        """
        log.info('Room quit <%s>', self)

        await self.puppet.room_quit(self.room_id)

    async def topic(self, new_topic: str = None) -> Optional[str]:
        """
        get/set room topic
        """
        log.info('Room topic (%s)', new_topic)

        if not self.is_ready():
            log.warning('Room topic() room not ready')
            raise Exception('Room not ready')

        if new_topic is None:
            if self.payload is not None and self.payload.topic is not None:
                return self.payload.topic

            # 获取名称之间的结合
            member_ids = await self.puppet.room_members(self.room_id)
            # filter member_ids
            member_ids = [member_id for member_id in member_ids
                          if member_id != self.puppet.self_id()]
            members: List[Contact] = list(
                map(lambda x: self.wechaty.Contact.load(x), member_ids)
            )
            names = [member.name for member in members]
            return ','.join(names)

        try:
            await self.puppet.room_topic(self.room_id, new_topic)
            return new_topic
        except Exception as exception:
            log.warning(
                'Room topic(newTopic=%s) exception: %s',
                new_topic,
                exception
            )
        return None

    async def announce(self, text: str = None) -> Optional[str]:
        """
        SET/GET announce from the room

        It only works when bot is the owner of the room.
        """

        log.info('Room announce (%s)', text)

        if text is None:
            announcement = await self.puppet.room_announce(self.room_id)
            return announcement
        await self.puppet.room_announce(self.room_id, text)
        return None

    async def qrcode(self) -> str:
        """
        TODO -> need to rewrite this function later
        Get QR Code Value of the Room from the room, which can be used as
        scan and join the room.
        """
        log.info('Room qr_code')
        qr_code_value = await self.puppet.room_qr_code(self.room_id)
        return qr_code_value

    async def alias(self, member: Contact) -> Optional[str]:
        """
        Return contact's roomAlias in the room
        """
        if member is None:
            raise Exception('member can"t be none')
        member_payload = await self.puppet.room_member_payload(
            self.room_id,
            member.contact_id
        )
        if member_payload is not None\
                and member_payload.room_alias is not None:
            return member_payload.room_alias
        return None

    async def has(self, contact: Contact) -> bool:
        """
        Check if the room has member `contact`, the return is a Promise and
        must be `await`-ed
        """
        member_ids = await self.puppet.room_members(self.room_id)
        if member_ids is None:
            return False

        return contact.contact_id in member_ids

    async def member_all(
        self, query: Union[str, RoomQueryFilter] = None
    ) -> List[Contact]:
        """
        Find all contacts in a room
        """
        log.info('room member all (%s)', json.dumps(query))
        if query is None:
            members = await self.member_list()
            return members

        contact_ids = await self.puppet.room_member_search()
        contacts = [
            self.wechaty.Contact.load(contact_id) for contact_id in contact_ids
        ]
        return contacts

    async def member_list(self) -> List[Contact]:
        """
        Get all room member from the room
        """
        log.info('Get room <%s> all members', self)

        member_ids = await self.puppet.room_members(self.room_id)
        if member_ids is None or len(member_ids) < 1:
            raise Exception(
                'Room <%s> member not found or room not found',
                self
            )

        contacts = [
            self.wechaty.Contact.load(member_id) for member_id in member_ids]

        return contacts

    async def member(
        self, query: Union[str, RoomQueryFilter] = None
    ) -> Optional[Contact]:
        """
        Find all contacts in a room, if get many, return the first one.
        """
        log.info('Room member search <%s>', query)

        members = await self.member_all(query)
        if members is None or len(members) < 1:
            return None
        return members[0]

    async def owner(self) -> Optional[Contact]:
        """
        get room owner
        """
        log.info('Room <%s> owner', self)
        if self.payload is None or self.payload.owner_id is None:
            # raise Exception('Room <%s> payload or payload.owner_id not found')
            return None

        contact = self.wechaty.Contact.load(self.payload.owner_id)
        return contact

    async def avatar(self) -> FileBox:
        """
        get the avatar of the room
        """
        log.info('Room <%s> avatar', self)

        avatar = await self.puppet.room_avatar(self.room_id)
        return avatar
