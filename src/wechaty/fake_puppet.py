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

from typing import List, Optional, Any, Dict
import asyncio
from uuid import uuid4
import random

from wechaty_puppet.file_box import FileBox

from wechaty_puppet.schemas.message import (
    MessageQueryFilter,
)
from wechaty_puppet.schemas.mini_program import (
    MiniProgramPayload
)
# pylint: disable=R0904
from wechaty_puppet import Puppet
from wechaty_puppet.schemas.puppet import PuppetOptions
from wechaty_puppet.schemas.event import EventLoginPayload
from wechaty_puppet.schemas.room import (
    RoomQueryFilter
)
from wechaty_puppet.schemas.url_link import UrlLinkPayload

from wechaty_puppet.schemas.types import (
    FriendshipPayload,
    ContactPayload,
    ImageType,
    MessagePayload,

    RoomPayload,
    RoomMemberPayload,

    RoomInvitationPayload,

    PayloadType

)
from pyee import AsyncIOEventEmitter


class FakeMixin:
    def get_fake_emitter(self) -> AsyncIOEventEmitter:
        """get fake emitter

        Returns:
            AsyncIOEventEmitter: get fake emitter
        """
        emitter = getattr(self, 'emitter', None)
        assert emitter is not None, 'emitter not found'
        assert isinstance(emitter, AsyncIOEventEmitter)
        return emitter

class FakeMessageManagerMixin(FakeMixin):
    def __init__(self) -> None:
        super().__init__(self)

        self._message_payloads: Dict[str, MessagePayload] = {}

    def add_fake_message(self, payload: MessagePayload):
        self._message_payloads[payload.id] = payload
    
    def get_fake_message(self, id: str) -> Optional[MessagePayload]:
        return self._message_payloads.get(id, None)
    
    def remove_fake_message(self, id: str):
        self._message_payloads.pop(id, None)
    
    def get_all_fake_messages(self) -> List[MessagePayload]:
        return list(self._message_payloads.values())
    
    def emit_fake_message(self, id: str):
        emitter = self.get_fake_emitter()
        message = self.get_fake_message(id)
        emitter.emit('message', message)

class FakeRoomManagerMixin(FakeMixin):
    def __init__(self) -> None:
        super().__init__(self)

        self._room_payloads: Dict[str, RoomPayload] = {}

    def get_all_fake_messages(self) -> List[RoomPayload]:
        return list(self._room_payloads.values())

    def add_fake_room(self, payload: RoomPayload):
        self._room_payloads[payload.id] = payload
    
    def get_fake_room(self, id: str) -> Optional[RoomPayload]:
        return self._room_payloads.get(id, None)
    
    def remove_fake_room(self, id: str):
        self._room_payloads.pop(id, None)

class FakeContactManagerMixin(FakeMixin):
    def __init__(self) -> None:
        super().__init__(self)

        self._contact_payloads: Dict[str, ContactPayload] = {}

    def get_all_fake_messages(self) -> List[ContactPayload]:
        return list(self._contact_payloads.values())

    def add_fake_contact(self, payload: ContactPayload):
        self._contact_payloads[payload.id] = payload
    
    def get_fake_contact(self, id: str) -> Optional[ContactPayload]:
        return self._contact_payloads.get(id, None)
    
    def remove_fake_contact(self, id: str):
        self._contact_payloads.pop(id, None)


class FakePuppet(Puppet, FakeContactManagerMixin, FakeMessageManagerMixin, FakeRoomManagerMixin):
    """
    puppet interface class, which is the abstract of puppet implementation.

    python-wechaty-puppet-XX can be all of the protocol of IM software.
    """

    def __init__(self, options: PuppetOptions, name: str = 'puppet') -> None:
        super().__init__(options, name)
        self.name: str = name
        self.options = options
        self.emitter = AsyncIOEventEmitter()
    
    def add_random_fake_contact_message(self, msg: Optional[str] = None, contact_id: Optional[str] = None) -> str:
        if not msg:
            msg = str(uuid4())
        if not contact_id:
            contact_id = random.choice(list(self._contact_payloads.keys()))
        
        message = MessagePayload(
            id=str(uuid4()),
            from_id=contact_id,
            text=msg
        )
        self.add_fake_message(message)
        return message.id
    
    def add_random_fake_room_message(self, msg: Optional[str] = None, contact_id: Optional[str] = None, room_id: Optional[str] = None) -> str:
        if not msg:
            msg = str(uuid4())
        if not contact_id and not room_id:
            payload: RoomPayload = random.choice(self._room_payloads.values())
            room_id = payload.id
            contact_id = random.choice(payload.member_ids)
        elif contact_id:
            for payload in self._room_payloads.values():
                if contact_id in payload.member_ids:
                    room_id = payload.id
                    break
        elif room_id:
            contact_id = self.get_fake_room(room_id).member_ids[0]
                
        message_payload = MessagePayload(
            id=str(uuid4()),
            from_id=contact_id,
            room_id=room_id,
            text=msg
        )
        self.add_fake_message(message_payload)
        return message_payload.id
    
    def add_random_fake_contact(self) -> str:
        payload = ContactPayload(
            id=str(uuid4()),
            name=str(uuid4()),
            friend=True
        )
        self.add_fake_contact(payload)
        return payload.id
    
    def add_random_fake_room(self) -> str:
        contact_ids = random.choices(list(self._contact_payloads.keys()), k=5)
        payload = RoomPayload(
            id=str(uuid4()),
            topic=str(uuid4()),
            member_ids=contact_ids,
            admin_ids=contact_ids[:2],
            owner_id=contact_ids[0],
        )
        self.add_fake_room(payload)
        return payload.id

    async def message_image(
            self,
            message_id: str,
            image_type: ImageType
    ) -> FileBox:
        """
        docstring
        :param message_id:
        :param image_type:
        :return:
        """

    async def ding(self, data: Optional[str] = None) -> None:
        """
        set the ding event
        :param data:
        :return:
        """
        self.emitter.emit('dong')

    def on(self, event_name: str, caller: Any) -> None:
        """register the event

        Args:
            event_name (str): the name of event
            caller (Any): the target call function
        """
        self.emitter.on(event_name, caller)

    def listener_count(self, event_name: str) -> int:
        """
        get the count of a specific event listener
        """
        return len(self.emitter.listeners(event_name))

    async def start(self) -> None:
        """
        start the puppet
        :return:
        """
        payload = EventLoginPayload(contact_id='fake-contact-id')

        self.emitter.emit('login', payload)
        while True:
            await asyncio.sleep(10)

    async def stop(self) -> None:
        """
        stop the puppet
        :return:
        """

    async def contact_list(self) -> List[str]:
        """
        get all contact list
        """
        return list(self._contact_payloads.keys())

    async def tag_contact_delete(self, tag_id: str) -> None:
        """
        :return:
        """

    async def tag_favorite_delete(self, tag_id: str) -> None:
        """
        delete favorite tag from favorite
        """

    async def tag_contact_add(self, tag_id: str, contact_id: str) -> None:
        """
        add tag to contact
        :param tag_id:
        :param contact_id:
        :return:
        """

    async def tag_favorite_add(self, tag_id: str, contact_id: str) -> None:
        """
        add tag to favorite
        """

    async def tag_contact_remove(self, tag_id: str, contact_id: str) -> None:
        """
        :param tag_id:
        :param contact_id:
        :return:
        """

    async def tag_contact_list(self, contact_id: Optional[str] = None) -> List[str]:
        """
        get tag list
        :return: tag_list
        """

    async def message_send_text(self, conversation_id: str, message: str,
                                mention_ids: List[str] = None) -> str:
        """
        send text message
        :param mention_ids:
        :param conversation_id: person contact_id or room_id
        :param message: message content
        :return: message_id
        """
        return 'static-id'

    async def message_send_contact(
            self,
            contact_id: str,
            conversation_id: str) -> str:
        """
        send contact message
        :param conversation_id:
        :param contact_id: person contact_id
        """
        return 'static-id'

    async def message_send_file(self, conversation_id: str, file: FileBox
                                ) -> str:
        """
        send file
        :param conversation_id:
        :param file: filebox instance
        """
        return 'static-id'

    async def message_send_url(
            self,
            conversation_id: str,
            url: str) -> str:
        """
        send url
        :param conversation_id:
        :param url: UrlLink instance
        """
        return 'static-id'

    async def message_send_mini_program(
            self,
            conversation_id: str,
            mini_program: MiniProgramPayload) -> str:
        """
        send mini_program message
        :param conversation_id:
        :param mini_program:
        :return:
        """
        return 'static-id'

    async def message_search(
            self,
            query: Optional[MessageQueryFilter] = None) -> List[str]:
        """
        search message
        """
        return list(self._message_payloads.keys())

    async def message_recall(self, message_id: str) -> bool:
        """
        send recall message
        :param message_id:
        :return:
        """
        return True

    async def message_payload(self, message_id: str) -> MessagePayload:
        """
        get message payload
        :param message_id:
        :return:
        """
        return self.get_fake_message(message_id)

    async def message_forward(self, to_id: str, message_id: str) -> None:
        """
        forward message
        :param to_id: type of Room/Contact
        :param message_id:
        :return:
        """

    async def message_file(self, message_id: str) -> FileBox:
        """
        convert message to filebox
        :param message_id:
        :return:
        """
        payload = self.get_fake_message(message_id)
        file_box = FileBox.from_json(payload.text)
        return file_box

    async def message_contact(self, message_id: str) -> str:
        """
        get message's contact card
        :param message_id:
        :return:
        """
        payload = self.get_fake_message(message_id)
        return payload.from_id

    async def message_url(self, message_id: str) -> UrlLinkPayload:
        """
        get message' url payload
        :param message_id:
        :return:
        """

    async def message_mini_program(self, message_id: str) -> MiniProgramPayload:
        """
        get message payload
        :param message_id:
        :return:
        """

    async def contact_alias(self, contact_id: str,
                            alias: Optional[str] = None) -> str:
        """
        set contact alias
        """
        contact = self.get_fake_contact(contact_id)
        if alias is not None:
            contact.alias = alias
            self.add_fake_contact(contact)
            return alias
        
        return contact.alias

    async def contact_payload_dirty(self, contact_id: str) -> None:
        """
        refresh contact payload
        """

    async def contact_payload(self, contact_id: str) -> ContactPayload:
        """
        get contact payload
        """
        return self.get_fake_contact(contact_id)

    async def contact_avatar(self, contact_id: str,
                             file_box: Optional[FileBox] = None
                             ) -> FileBox:
        """
        get the avatar of the account
        """

    async def contact_tag_ids(self, contact_id: str) -> List[str]:
        """
        get tag_ids of the account
        """

    def self_id(self) -> str:
        """
        get self_id
        """

    async def friendship_search(self, weixin: Optional[str] = None,
                                phone: Optional[str] = None
                                ) -> Optional[str]:
        """
        search friend by query
        :params:
        :return:
        """

    async def friendship_add(self, contact_id: str, hello: str) -> None:
        """
        add friendship with hello
        """

    async def friendship_payload(
            self,
            friendship_id: str,
            payload: Optional[FriendshipPayload] = None) -> FriendshipPayload:
        """
        load friendship payload
        """

    async def friendship_accept(self, friendship_id: str) -> None:
        """
        accept friendship
        """

    async def room_list(self) -> List[str]:
        """
        get room list
        :return:
        """
        return list(self._room_payloads.keys())

    async def room_create(self, contact_ids: List[str], topic: str = None
                          ) -> str:
        """
        create room with contact_ids and topic
        """
        room_payload = RoomPayload(
            id=str(uuid4()),
            topic=topic,
            member_ids=contact_ids,
            admin_ids=contact_ids[:1],
            owner_id=contact_ids[0]
        )
        self.add_fake_room(room_payload)

    async def room_search(self, query: RoomQueryFilter = None) -> List[str]:
        """
        search room by query filter
        """
        return list(self._room_payloads.keys())

    async def room_invitation_payload(self, room_invitation_id: str,
                                      payload: Optional[RoomInvitationPayload]
                                      = None) -> RoomInvitationPayload:
        """
        get room invitation payload
        """

    async def room_invitation_accept(self, room_invitation_id: str) -> None:
        """
        get room invitation payload
        """

    async def contact_self_qr_code(self) -> str:
        """
        get login qrcode
        """

    async def contact_self_name(self, name: str) -> None:
        """
        change bot contact name
        """

    async def contact_signature(self, signature: str) -> None:
        """
        change signature
        """

    async def room_payload(self, room_id: str) -> RoomPayload:
        """
        get room payload
        """
        return self.get_fake_room(room_id)

    async def room_members(self, room_id: str) -> List[str]:
        """
        get room members
        """
        payload = self.get_fake_room(room_id)
        return payload.member_ids

    async def room_add(self, room_id: str, contact_id: str) -> None:
        """
        add contact to a room
        """
        payload = self.get_fake_room(room_id)
        if contact_id not in payload.member_ids:
            payload.member_ids.append(contact_id)
        self.add_fake_room(payload)

    async def room_delete(self, room_id: str, contact_id: str) -> None:
        """
        delete room
        """
        payload = self.get_fake_room(room_id)
        if contact_id in payload.member_ids:
            index = payload.member_ids.index(contact_id)
            payload.member_ids.pop(index)
            self.add_fake_room(payload)

    async def room_quit(self, room_id: str) -> None:
        """
        quit from
        """
        self.remove_fake_room(room_id)

    async def room_topic(self, room_id: str, new_topic: str) -> None:
        """
        set room topic
        """
        payload = self.get_fake_room(room_id)
        if new_topic:
            payload.topic = new_topic
            self.add_fake_room(payload)

    async def room_announce(
            self,
            room_id: str,
            announcement: str = None) -> str:
        """
        set/get room announcement
        """

    async def room_qr_code(self, room_id: str) -> str:
        """
        get room_qrcode
        """

    async def room_member_payload(
            self,
            room_id: str,
            contact_id: str) -> RoomMemberPayload:
        """
        get room member payload
        """
        return self.get_fake_contact(contact_id)

    async def room_avatar(self, room_id: str) -> FileBox:
        """
        get the avatar of the room
        """

    async def logout(self) -> None:
        """
        logout the account
        :return:
        """

    async def login(self, user_id: str) -> None:
        """
        login the account
        :return:
        """

    async def dirty_payload(self, payload_type: PayloadType, payload_id: str) -> None:
        """
        mark the payload dirty status, and remove
        """
