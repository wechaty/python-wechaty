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
from typing import (
    Optional,
    Union,
    List
)
import json

from wechaty_puppet.message import (
    MessagePayload,
    MessageQueryFilter,
    MessageType
)

from ..accessory import Accessory
from ..config import (
    log,
    FileBox
)
from .contact import Contact
from .room import Room
from .url_link import UrlLink
from .mini_program import MiniProgram
from .image import Image
from ..types import Sayable


class MessageUserQueryFilter:
    """
    doc
    """
    def __init__(
            self,
            text: Optional[str] = None,
            room: Optional[Room] = None,
            type: Optional[MessageType] = None,
            talker: Optional[Contact] = None,
            to: Optional[Contact] = None):
        """
        initialization
        """
        # from is a keyword in python, so we should change it
        self.talker: Optional[Contact] = None
        self.text: Optional[str] = text
        self.room: Optional[Room] = None
        self.type: Optional[MessageType] = None
        self.to: Optional[Contact] = None


def _convert_message(
        user_query: MessageUserQueryFilter = None) -> Optional[MessageQueryFilter]:
    """
    convert wechaty message_user_query_filter
        to wechaty_puppet message_query_filter
    """
    if user_query is None:
        return None
    
    query = MessageQueryFilter(text=user_query.text)

    if user_query.room is not None:
        query.room_id = user_query.room.room_id

    if user_query.talker is not None:
        query.talker_id = user_query.talker.contact_id

    if user_query.type is not None:
        query.type = user_query.type

    if user_query.to is not None:
        query.to_id = user_query.to.contact_id

    return query


# pylint: disable=R0903
class Message(Accessory, Sayable):
    """
    All wechat messages will be encapsulated as a Message.
    """

    Type = MessageType

    def __init__(self, message_id: str):
        """
        initialization
        """
        log.info(
            'Message constructor(%s) for class Message (%s)',
            self.__class__.__name__,
            message_id)
        self.message_id = message_id
        self._message_payload: Optional[MessagePayload] = None


        # TODO -> check if it's Message class
        if not issubclass(self.__class__, Message):
            raise Exception("Message class can not be instanciated directly!")

        if self.puppet is None:
            raise Exception("Message class can not be instanciated without a puppet!")
    
    @property
    def payload(self) -> Optional[MessagePayload]:
        """
        get message payload
        """
        return self._message_payload

    def message_type(self) -> MessageType:
        """
        get message type
        """
        if self.payload is None:
            raise Exception("MessagePayload not found ...")
        return self.payload.type
    
    def __str__(self) -> str:
        """
        format string for message
        """
        if self.payload is not None:
            return self.__class__.__name__
        # TODO -> check condition string format
        return ''

    async def say(
            self, text: str,
            reply_to: Union[Contact, List[Contact]]
    ) -> Optional[Message]:
        """
        send message
        """
        raise NotImplementedError

    @classmethod
    async def find(
            cls,
            # need return type annotation
            query: Union[str, MessageUserQueryFilter]):
        """
        Find message in cache
        """
        log.info("Message find <%s>", json.dumps(query))
        if isinstance(query, str):
            query = MessageUserQueryFilter(text=query)

        messages = await cls.find_all(query)
        if messages is None or len(messages) < 1:
            return None

        if len(messages) > 1:
            log.warn(
                'Message findAll() got more than one(%d) result',
                len(messages))
        return messages[0]

    @classmethod
    async def find_all(
            cls,
            query: MessageUserQueryFilter = None) -> List[Message]:
        """
        Find messages in cache
        """
        log.info("Message find all <%s>", json.dumps(query))

        # use query_filter to change query filter type
        query_filter: Optional[MessageQueryFilter] = None
        if query is not None:
            query_filter = _convert_message(query)

        message_ids = await cls.get_puppet().message_search(query_filter)
        try:
            messages = [cls.load(message_id) for message_id in message_ids]

            # TODO:multi process for load message instance
            async def load_message(msg: Message):
                await msg.ready()
            messages = [await load_message(message) for message in messages]
            return list(filter(lambda msg: msg.is_ready(), messages))
        except Exception as e:
            log.error(
                'Message findAll() rejected: %s',
                json.dumps(e.args))
            return []

    def talker(self) -> Optional[Contact]:
        """
        get message talker

        # TODO ->   Suggestion: talker/to/room/text func can
        #           be converted to property func
        """
        if self.payload is None:
            raise Exception("Message payload not found ...")
        talker_id = self.payload.talker_id
        if talker_id is None:
            return None
        return self.wechaty.Contact.load(talker_id)
    
    def to(self) -> Optional[Contact]:
        """
        get message reply to
        """
        if self.payload is None:
            raise Exception("Message payload not found ...")
        to_id = self.payload.to_id
        if to_id is None:
            return None
        return self.wechaty.Contact.load(to_id)

    def room(self) -> Optional[Room]:
        """
        get message room
        """
        if self.payload is None:
            raise Exception("Message payload not found ...")
        room_id = self.payload.room_id
        if room_id is None:
            return None
        return self.wechaty.Room.load(room_id)
    
    def text(self) -> str:
        """
        get message text
        """
        if self.payload is None:
            raise Exception("Message payload not found ...")
        if self.payload.text is None:
            return ''
        return self.payload.text

    # TODO -> toRecalled

    @classmethod
    def load(cls, message_id: str) -> Message:
        """
        Create a Mobile Terminated Message
        """
        return cls(message_id)

    async def ready(self):
        """
        sync load message
        """
        raise NotImplementedError

    def is_ready(self):
        """
        check message is ready
        """
        raise NotImplementedError
