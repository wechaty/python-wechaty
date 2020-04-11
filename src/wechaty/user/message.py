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
    List,
    TYPE_CHECKING,
)

from dataclasses import dataclass
from datetime import datetime
import json
from wechaty_puppet import (
    MessagePayload,
    MessageQueryFilter,
    MessageType
)

from ..accessory import Accessory

from .room import Room
from .mini_program import MiniProgram
from ..types import Sayable
from ..log import WechatyLogger

if TYPE_CHECKING:
    from .contact import Contact
    from .url_link import UrlLink
    from .image import Image

    from wechaty_puppet import (
        FileBox
    )

log = WechatyLogger('Message')


@dataclass
class MessageUserQueryFilter:
    """
    doc
    """
    text  : Optional[str]         = None
    room  : Optional[Room]        = None
    type  : Optional[MessageType] = None
    talker: Optional[Contact]     = None
    to    : Optional[Contact]     = None


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

    @log
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
    @log
    async def find(
            cls,
            # need return type annotation
            query: Union[str, MessageUserQueryFilter]):
        """
        Find message in cache
        """
        if isinstance(query, str):
            query = MessageUserQueryFilter(text=query)

        messages = await cls.find_all(query)
        if messages is None or len(messages) < 1:
            return None

        if len(messages) > 1:
            log.warning(
                'Message findAll() got more than one(%d) result',
                len(messages))
        return messages[0]

    @classmethod
    @log
    async def find_all(
            cls,
            query: MessageUserQueryFilter = None) -> List[Message]:
        """
        Find messages in cache
        """
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

    async def to_recalled(self) -> Message:
        """
        Get the recalled message
        """
        if self.message_type() != MessageType.Recalled:
            raise Exception(
                "Can not call toRecalled() on message which is not"
                " recalled type.")

        origin_message_id = self.text()
        if origin_message_id is None:
            raise Exception("Can not find recalled message")

        log.info("get recall message <%s>", origin_message_id)
        try:
            message = self.wechaty.Message.load(origin_message_id)
            await message.ready()
            return message
        except Exception as exception:
            error_info = "can't load or ready message payload {}".format(
                str(exception.args)
            )

            log.error(error_info)
            raise Exception(error_info)

    async def recall(self) -> bool:
        """
        Recall a message.
        """
        log.info('Message recall')
        recall_result = await self.puppet.message_recall(self.message_id)
        return recall_result

    @classmethod
    def load(cls, message_id: str) -> Message:
        """
        Create a Mobile Terminated Message
        """
        return cls(message_id)

    def type(self) -> MessageType:
        """
        Get the type from the message.
        :return:
        """
        if self.payload is None:
            raise Exception('payload not found')
        return self.payload.type

    def is_self(self) -> bool:
        """
        Check if a message is sent by self
        :return:
        """
        user_id = self.puppet.self_id()
        talker = self.talker()
        if talker is None:
            return False
        return talker.contact_id == user_id

    @log
    async def mention_list(self) -> List[Contact]:
        """
        Get message mentioned contactList.
        :return:
        """
        room = self.room()
        if self.type() != MessageType.Text or room is None:
            return []
        """
        Use mention list if mention list is available
        otherwise, process the message and get the mention list
        """
        if self.payload is not None and self.payload.mention_ids is not None:
            async def id_to_contact(contact_id) -> Contact:
                contact = await self.wechaty.Contact.load(contact_id)
                await contact.ready()
                return contact
            # TODO -> change to python async best practice
            contacts = [
                await id_to_contact(contact_id)
                for contact_id in self.payload.mention_ids]
            return contacts

        # TODO -> have to check that mention_id is not in room situation
        return []

    async def mention_text(self) -> str:
        """
        get mention text
        :return:
        """
        text = self.text()
        room = self.room()

        mention_list = await self.mention_list()

        if room is None or len(mention_list) <= 0:
            return text

        async def get_alias_or_name(member: Contact) -> str:
            if room is not None:
                alias = await room.alias(member)
                if alias is not None:
                    return alias
            return member.name

        # TODO -> change to python async best practice
        # flake8: disable=F841
        mention_names = [
            await get_alias_or_name(member)
            for member in mention_list]
        # TOD -> need to remove
        reversed(mention_names)
        """
        const textWithoutMention = mentionNameList.reduce((prev, cur) => {
            const escapedCur = escapeRegExp(cur)
            const regex = new RegExp(`@${escapedCur}(\u2005|\u0020|$)`)
            return prev.replace(regex, '')
        }, text)
        """
        # import re
        # from functools import reduce
        # def reg_replace(pre, cur) -> str:
        #     regex =
        return ''

    async def mention_self(self) -> bool:
        """
        Check if a message is mention self.
        :return:
        """
        self_id = self.puppet.self_id()

        # check and ready for message payload
        self.ready()

        # check by mention_ids not mention_list
        if self.payload is None or self.payload.mention_ids is None:
            return False
        return self_id in self.payload.mention_ids

    @log
    async def ready(self):
        """
        sync load message
        """
        log.info('Message ready()')
        if self.is_ready():
            return

        payload = await self.puppet.message_payload(self.message_id)

        if self.payload is None:
            raise Exception("payload not found")

        self._message_payload = payload

        if self.payload.talker_id is not None:
            await self.wechaty.Contact.load(self.payload.talker_id)
        if self.payload.room_id is not None:
            await self.wechaty.Room.load(self.payload.room_id)
        if self.payload.to_id is not None:
            await self.wechaty.Contact.load(self.payload.to_id)

    def is_ready(self) -> bool:
        """
        check message is ready
        """
        return self.payload is not None

    @log
    async def forward(self, to: Union[Room, Contact]):
        """
        doc
        :param to:
        :return:
        """
        if to is None:
            raise Exception("to param not found")
        try:
            if isinstance(to, Room):
                to_id = to.room_id
            elif isinstance(to, Contact):
                to_id = to.contact_id
            else:
                raise Exception(
                    'expected type is <Room, Contact>, but get <%s>',
                    to.__class__)
            await self.puppet.message_forward(to_id, self.message_id)
        except Exception as exception:
            log.error(
                'Message forward error <%s>',
                exception.args
            )

    def date(self) -> datetime:
        """
        Message sent date
        :return:
        """
        if self.payload is None:
            raise Exception("payload not found")
        return self.payload.timestamp

    def age(self) -> int:
        """
        Returns the message age in seconds.
        :return:
        """
        if self.payload is None:
            raise Exception("Message payload not found")
        return (datetime.now() - self.payload.timestamp).seconds // 1000

    @log
    async def to_file_box(self) -> FileBox:
        """
        Extract the Media File from the Message, and put it into the FileBox.
        """
        if self.type() == MessageType.Text:
            raise Exception('text message can"t convert to FileBox')
        file_box = await self.puppet.message_file(self.message_id)
        return file_box

    def to_image(self) -> Image:
        """
        Extract the Image File from the Message, so that we can use
        different image sizes.
        :return:
        """
        log.info('Message to Image() for message %s', self.message_id)
        if self.type() != MessageType.Image:
            raise Exception(
                'current message type: %s, not image type',
                self.type()
            )
        return self.wechaty.Image.create(self.message_id)

    @log
    async def to_contact(self) -> Contact:
        """
        Get Share Card of the Message
        Extract the Contact Card from the Message, and encapsulate it into Contact class
        :return:
        """
        if self.type() != MessageType.Contact:
            raise Exception(
                'current message type: %s, not contact type',
                self.type()
            )

        contact_id = await self.puppet.message_contact(self.message_id)
        if contact_id is None:
            raise Exception(
                'can not get Contact id by message: %s',
                self.message_id)

        contact = self.wechaty.Contact.load(contact_id)
        await contact.ready()
        return contact

    @log
    async def to_url_link(self) -> UrlLink:
        """
        get url_link from message
        :return:
        """
        if self.type() != MessageType.Url:
            raise Exception(
                'current message type: %s, not url type',
                self.type()
            )

        payload = await self.puppet.message_url(self.message_id)
        if payload is None:
            raise Exception(
                'can not get url_link_payload by message: %s',
                self.message_id)
        return UrlLink(payload)

    async def to_mini_program(self) -> MiniProgram:
        """
        get message mini_program
        :return:
        """
        log.info('Message to MiniProgram <%s>', self.message_id)

        if self.payload is None:
            raise Exception('payload not found')

        if self.type() != MessageType.MiniProgram:
            raise Exception('not a mini_program type message')

        payload = await self.puppet.message_mini_program(self.message_id)

        if payload is None:
            raise Exception(
                'no miniProgram payload for message %s',
                self.message_id
            )
        return MiniProgram(payload)
