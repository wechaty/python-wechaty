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

import asyncio
import dataclasses
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
from pyee import AsyncIOEventEmitter  # type: ignore
# from wechaty_puppet import RoomMemberPayload
from wechaty.exceptions import WechatyOperationError, WechatyPayloadError
from wechaty_puppet import (  # type: ignore
    FileBox,
    RoomQueryFilter,
    RoomMemberQueryFilter,
    RoomPayload,
    get_logger
)
# from wechaty.utils import type_check
from ..accessory import Accessory

if TYPE_CHECKING:
    from .contact import Contact
    from .url_link import UrlLink
    from .mini_program import MiniProgram
    from .message import Message

log = get_logger('Room')


class Room(Accessory[RoomPayload]):
    """
    All wechat rooms(groups) will be encapsulated as a Room.
    """
    _pool: Dict[str, 'Room'] = defaultdict()

    def __init__(self, room_id: str) -> None:
        """docs"""
        super().__init__()

        self.room_id = room_id

    _event_stream: AsyncIOEventEmitter = AsyncIOEventEmitter()

    def on(self, event_name: str, func):
        """
        listen event for contact
        event_name:
        """
        self._event_stream.on(event_name, func)

    def emit(self, event_name: str, *args, **kwargs):
        """
        emit event for a specific
        """
        self._event_stream.emit(event_name, *args, **kwargs)

    @classmethod
    async def create(cls, contacts: List[Contact], topic: str) -> Room:
        """
        create room instance
        """
        if not hasattr(contacts, '__len__'):
            raise WechatyOperationError('contacts should be list type')
        if len(contacts) < 2:
            raise WechatyOperationError(
                'contactList need at least 2 contact to create a new room'
            )

        log.info(
            'Room create <%s - %s>',
            ','.join([contact.contact_id for contact in contacts]),
            topic
        )

        try:
            contact_ids = list(map(lambda x: x.contact_id, contacts))
            room_id = await cls.get_puppet(). \
                room_create(contact_ids=contact_ids, topic=topic)
            room = cls.load(room_id=room_id)
            await room.ready()
            return room
        except Exception as exception:
            message = 'Room create error <%s>' % str(exception.args)
            log.error(message)
            raise WechatyOperationError(message)

    @classmethod
    async def find_all(cls,
                       query: Union[str, RoomQueryFilter] = None) -> List[Room]:
        """
        find room by query filter

        TODO -> we should remove search_query from puppet-*
        """
        log.info('Room find_all <%s>', query)

        room_ids = await cls.get_puppet().room_search()
        rooms = [cls.load(room_id) for room_id in room_ids]

        # using async parallel pattern to load room payload
        await asyncio.gather(*[room.ready() for room in rooms])

        # search by any field contains query word
        if query is not None:
            if isinstance(query, str):
                rooms = list(
                    filter(
                        lambda x: False if not x.payload else
                        (x.payload.id.__contains__(query)) or
                        (x.payload.topic.__contains__(query)),
                        rooms
                    )
                )

            if isinstance(query, RoomQueryFilter):
                newQuery: Dict = dataclasses.asdict(query)
                rooms = list(
                    filter(
                        lambda x: False if not x.payload else
                        (x.payload.id == newQuery.get('id') or not newQuery.get('id')) and
                        (x.payload.topic == newQuery.get('topic') or not newQuery.get('topic')),
                        rooms
                    )
                )
        return rooms

    @classmethod
    async def find(cls,
                   query: Union[str, RoomQueryFilter] = None) -> Union[None, Room]:
        """
        Try to find a room by filter: {topic: string | RegExp}. If get many,
        return the first one.
        """
        log.info('Room find <%s>', query)

        rooms = await cls.find_all(query)

        if rooms is None or len(rooms) < 1:
            return None

        if len(rooms) > 1:
            log.warning('Room find() got more than one(%d) result', len(rooms))

        for index, room in enumerate(rooms):
            # TODO -> room_valid function is not implemented in puppet
            # this code need to be changed later

            valid = cls.get_puppet() is not None

            if valid:
                log.warning(
                    'Room find() confirm room[#%d] with id=%s '
                    'is valid result, return it.',
                    index,
                    room.room_id
                )
                return room
            log.info(
                'Room find() confirm room[#%d] with id=%s '
                'is INVALID result, try next',
                index,
                room.room_id)
        log.info('Room find() got %d rooms but no one is valid.', len(rooms))
        return None

    @classmethod
    def load(cls, room_id: str) -> Room:
        """
        dynamic load room instance
        """
        room = cls._pool.get(room_id)
        if room is not None:
            return room

        room = cls(room_id)
        cls._pool[room_id] = room
        return room

    def __str__(self):
        """
        string format for room instance
        """
        if self.payload is None:
            return self.__class__.__name__

        if self.payload.topic is None:
            return 'loading ...'

        return 'Room <%s - %s>' % (self.room_id, self.payload.topic)

    async def ready(self, force_sync=False):
        """
        Please not to use `ready()` at the user land.
        """
        if self.is_ready():
            return

        if force_sync:
            self.payload = None

            # TODO -> *_dirty method is not implemented in puppet
            # await self.puppet.room_payload_dirty(self.room_id)
            # await self.puppet.room_member_payload_dirty(self.room_id)

        self.payload = await self.puppet.room_payload(self.room_id)

        if self.payload is None:
            raise WechatyPayloadError('Room Payload can"t be ready')

        member_ids = await self.puppet.room_members(self.room_id)

        contacts = [
            self.wechaty.Contact.load(member_id) for member_id in member_ids]

        for contact in contacts:
            try:
                await contact.ready()
            # pylint:disable=W0703
            except Exception as exception:
                log.error(
                    'Room ready() member.ready() rejection: %s', exception
                )

    async def say(self,
                  some_thing: Union[str, Contact,
                                    FileBox, MiniProgram, UrlLink],
                  mention_ids: Optional[List[str]] = None
                  ) -> Union[None, Message]:
        """
        Room Say(%s, %s)
        """
        log.info('Room say <%s, %s>', some_thing, mention_ids)

        if not some_thing:
            log.error('can"t say nothing')
            return None

        # we should import UrlLink type locally because of circular dependency

        from wechaty.user.url_link import UrlLink
        from wechaty.user.mini_program import MiniProgram
        from wechaty.user.contact import Contact
        if isinstance(some_thing, str):
            msg_id = await self.puppet.message_send_text(
                conversation_id=self.room_id, message=some_thing,
                mention_ids=mention_ids
            )
        elif isinstance(some_thing, FileBox):
            msg_id = await self.puppet.message_send_file(
                conversation_id=self.room_id,
                file=some_thing
            )
        elif isinstance(some_thing, Contact):
            msg_id = await self.puppet.message_send_contact(
                conversation_id=self.room_id,
                contact_id=some_thing.contact_id
            )
        elif isinstance(some_thing, UrlLink):
            msg_id = await self.puppet.message_send_url(
                conversation_id=self.room_id,
                url=json.dumps(dataclasses.asdict(some_thing.payload))
            )
        elif isinstance(some_thing, MiniProgram):
            # TODO -> mini_program key is not clear
            assert some_thing.payload is not None
            msg_id = await self.puppet.message_send_mini_program(
                conversation_id=self.room_id,
                mini_program=some_thing.payload
            )
        else:
            raise WechatyOperationError('arg unsupported: ', some_thing)

        if msg_id is not None:
            msg = self.wechaty.Message.load(msg_id)
            await msg.ready()
            return msg
        return None

    # '''
    # TODO -> sayTemplateStringsArray
    # '''

    # '''
    # TODO -> Event emit : on
    # '''

    # async def on(self, event: str, listener: Callable):

    async def add(self, contact: Contact):
        """
        Add contact in a room
        """
        log.info('Room add <%s>', contact)

        await self.puppet.room_add(self.room_id, contact.contact_id)
        # reload the payload
        await self.ready(force_sync=True)

    async def delete(self, contact: Contact):
        """
        delete room
        """
        log.info('Room delete<%s>', contact)

        if contact is None or contact.contact_id is None:
            raise WechatyOperationError('Contact is none or contact_id not found')
        await self.puppet.room_delete(self.room_id, contact.contact_id)
        # reload the payload
        await self.ready(force_sync=True)

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

        await self.ready()

        if new_topic is None:
            if self.payload is not None and self.payload.topic is not None:
                return self.payload.topic

            # 获取名称之间的结合
            room_member_ids = await \
                self.puppet.room_members(self.room_id)
            # filter member_ids
            member_ids = [member_id for member_id in
                          room_member_ids
                          if member_id != self.wechaty.contact_id]

            members: List[Contact] = [
                self.wechaty.Contact.load(member_id)
                for member_id in member_ids]

            for member in members:
                await member.ready()

            names = [member.name for member in members]
            return ','.join(names)

        try:
            await self.puppet.room_topic(self.room_id, new_topic)
            # reload the payload
            await self.ready(force_sync=True)
            return new_topic
        # pylint:disable=W0703
        except Exception as exception:
            log.warning(
                'Room topic(newTopic=%s) exception: %s',
                new_topic,
                exception
            )
        return None

    async def announce(self, announce_text: str = None) -> Optional[str]:
        """
        SET/GET announce from the room

        It only works when bot is the owner of the room.
        """

        log.info('Room announce (%s)', announce_text)

        if announce_text is None:
            announce = await self.puppet.room_announce(self.room_id)
            return announce
        await self.puppet.room_announce(self.room_id, announce_text)
        # reload the payload
        await self.ready(force_sync=True)
        return None

    async def qr_code(self) -> str:
        """
        TODO -> need to rewrite this function later
        Get QR Code Value of the Room from the room, which can be used as
        scan and join the room.

        'Wechaty Puppet Unsupported API Error. Learn More At
        https://github.com/wechaty/wechaty-puppet/wiki/Compatibility', None)>

        """
        log.info('qr_code()')
        qr_code_str = await self.puppet.room_qr_code(self.room_id)
        return qr_code_str

    async def alias(self, member: Contact) -> Optional[str]:
        """
        Return contact's roomAlias in the room

        TODO -> 'Wechaty Puppet Unsupported API Error. Learn More At
        https://github.com/wechaty/wechaty-puppet/wiki/Compatibility', None)>

        the result of the function will always return an empty string
        """
        if member is None:
            raise WechatyOperationError('member can"t be none')
        room_member_payload = await self.puppet.room_member_payload(
            room_id=self.room_id, contact_id=member.contact_id)

        if room_member_payload is not None \
            and room_member_payload.room_alias is not None:
            return room_member_payload.room_alias
        return None

    async def has(self, contact: Contact) -> bool:
        """
        Check if the room has member `contact`, the return is a Promise and
        must be `await`-ed
        """
        if self.payload is None:
            await self.ready()
            assert self.payload is not None
        return contact.contact_id in self.payload.member_ids

    async def member_list(self,
                          query: Union[str, RoomMemberQueryFilter] = None
                          ) -> List[Contact]:
        """
        Get all room member from the room
        """
        log.info('Get room <%s> all members', self)

        member_ids = await self.puppet.room_members(self.room_id)
        members: List[Contact] = [
            self.wechaty.Contact.load(member_id)
            for member_id in member_ids
        ]
        await asyncio.gather(*[member.ready() for member in members])

        if query is not None:
            if isinstance(query, str):
                member_search_result = []
                for member in members:

                    if member.payload is not None:
                        if member.name.__contains__(query):
                            member_search_result.append(member)
                        elif member.payload.alias is not None and \
                            member.payload.alias.__contains__(query):
                            member_search_result.append(member)

                    # get room_alias but hostie-server not support
                return member_search_result

            if isinstance(query, RoomMemberQueryFilter):
                member_search_result = []
                for member in members:
                    if member.payload is not None:
                        if member.name.__contains__(query.name):
                            member_search_result.append(member)

                        elif member.payload.alias is not None and \
                            member.payload.alias.__contains__(
                                query.contact_alias):

                            member_search_result.append(member)

                    # get room_alias but hostie-server not support
                return member_search_result

        return members

    async def member(self,
                     query: Union[str, RoomMemberQueryFilter] = None
                     ) -> Optional[Contact]:
        """
        Find all contacts in a room, if get many, return the first one.

        # TODO -> need to refactoring this function

        """
        log.info('Room member search <%s>', query)

        members = await self.member_list(query)
        if members is None or len(members) < 1:
            return None
        return members[0]

    async def owner(self) -> Optional[Contact]:
        """
        get room owner
        """
        log.info('Room <%s> owner', self)
        await self.ready()

        if self.payload.owner_id is None or self.payload.owner_id == '':
            # raise Exception('Room <%s> payload or payload.owner_id not found')
            return None

        contact = self.wechaty.Contact.load(self.payload.owner_id)
        return contact

    async def avatar(self) -> FileBox:
        """
        get the avatar of the room
        """
        log.info('avatar() <%s>', self)

        avatar = await self.puppet.room_avatar(self.room_id)
        return avatar
