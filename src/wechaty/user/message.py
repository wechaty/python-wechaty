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
)

from datetime import datetime
from wechaty_puppet import (    # type: ignore
    FileBox,
    MessagePayload,
    MessageQueryFilter,
    MessageType,
    get_logger
)

from ..accessory import Accessory
from .mini_program import MiniProgram
# TODO -> remove Sayable interface temporary
# from ..types import Sayable

from .contact import Contact
from .url_link import UrlLink
from .image import Image
from .room import Room

log = get_logger('Message')


# pylint: disable=R0904,R0903
class Message(Accessory):
    """
    All wechat messages will be encapsulated as a Message.
    """

    Type = MessageType

    def __init__(self, message_id: str):
        """
        initialization
        """
        self.message_id = message_id
        self._payload: Optional[MessagePayload] = None

        # TODO -> check if it's Message class
        if not issubclass(self.__class__, Message):
            raise Exception('Message class can not be Initialized directly!')

        if self.puppet is None:
            raise Exception(
                'Message class can not be Initialized without a puppet!'
            )

    @property
    def payload(self) -> Optional[MessagePayload]:
        """
        get message payload
        """
        return self._payload

    def message_type(self) -> MessageType:
        """
        get message type
        """
        if self.payload is None:
            raise Exception('MessagePayload not found ...')
        return self.payload.type

    def __str__(self) -> str:
        """
        format string for message
        """
        if self.payload is not None:
            room = self.room()
            room_format = '' if room is None \
                else f'room <{room}>, '

            to = self.to()
            to_format = '' if to is None \
                else f'say to contact <{to}>'
            return '%stalker %s, %s, %s' % (
                room_format,
                self.talker(),
                to_format,
                self.text(),
            )
        return f'<{self.message_id}> not ready'

    async def say(self, msg: Union[str, Contact, FileBox, UrlLink, MiniProgram],
                  mention_ids: Optional[List[str]] = None) -> Message:
        """
        send message
        """
        log.info('say() <%s>', msg)

        room = self.room()
        if room is not None:
            conversation_id = room.room_id
        else:
            talker = self.talker()
            if talker is None:
                raise ValueError(f'Message must be from room/contact')
            conversation_id = talker.contact_id

        # in order to resolve circular dependency problems which is not for
        # typing, we import some modules locally.
        # TODO -> this is not good solution, we will fix it later.

        from .url_link import UrlLink
        from .mini_program import MiniProgram

        if isinstance(msg, str):
            message_id = await self.puppet.message_send_text(
                conversation_id=conversation_id,
                message=msg,
                mention_ids=mention_ids)

        elif isinstance(msg, Contact):
            message_id = await self.puppet.message_send_contact(
                conversation_id=conversation_id, contact_id=msg.contact_id)
        elif isinstance(msg, FileBox):
            message_id = await self.puppet.message_send_file(
                conversation_id=conversation_id, file=msg)
        elif isinstance(msg, UrlLink):
            message_id = await self.puppet.message_send_url(
                conversation_id=conversation_id, url=msg.url)
        elif isinstance(msg, MiniProgram):
            assert msg.payload is not None
            message_id = await self.puppet.message_send_mini_program(
                conversation_id=conversation_id,
                mini_program=msg.payload)
        else:
            raise ValueError(f'message type should be str, '
                             f'Contact/FileBox/UrlLink/MiniProgram')

        message = self.load(message_id)
        await message.ready()
        return message

    @classmethod
    async def find(cls, talker_id: Optional[str] = None,
                   message_id: Optional[str] = None,
                   room_id: Optional[str] = None,
                   text: Optional[str] = None,
                   to_id: Optional[str] = None,
                   message_type: Optional[MessageType] = None
                   ) -> Optional[Message]:
        """
        Find message in cache
        """
        log.info('Message find all <%s, %s, %s, <%s, %s, %s>', talker_id,
                 message_id, room_id, text, to_id, message_type)

        messages = await cls.find_all(
            talker_id=talker_id,
            message_id=message_id,
            room_id=room_id,
            text=text,
            to_id=to_id,
            message_type=message_type
        )
        if messages is None or len(messages) < 1:
            return None

        if len(messages) > 1:
            log.warning(
                'Message findAll() got more than one(%d) result',
                len(messages))
        return messages[0]

    @classmethod
    async def find_all(cls, talker_id: Optional[str] = None,
                       message_id: Optional[str] = None,
                       room_id: Optional[str] = None,
                       text: Optional[str] = None,
                       to_id: Optional[str] = None,
                       message_type: Optional[MessageType] = None
                       ) -> List[Message]:
        """
        Find messages in cache
        """
        log.info('Message find all <%s, %s, %s, <%s, %s, %s>', talker_id,
                 message_id, room_id, text, to_id, message_type)

        query_filter = MessageQueryFilter(
            from_id=talker_id,
            id=message_id,
            room_id=room_id,
            text=text,
            to_id=to_id,
            type=message_type
        )
        message_ids = await cls.get_puppet().message_search(query_filter)
        messages = [cls.load(message_id) for message_id in message_ids]
        return messages

    def talker(self) -> Contact:
        """
        get message talker

        # TODO ->   Suggestion: talker/to/room/text func can
        #           be converted to property func
        """
        if self.payload is None:
            raise Exception('Message payload not found ...')
        talker_id = self.payload.from_id
        if talker_id is None:
            raise ValueError(f'message must be from Contact')
        return self.wechaty.Contact.load(talker_id)

    def to(self) -> Optional[Contact]:
        """
        get message reply to
        """
        if self.payload is None:
            raise Exception('Message payload not found ...')
        to_id = self.payload.to_id
        if to_id is None:
            return None
        return self.wechaty.Contact.load(to_id)

    def room(self) -> Optional[Room]:
        """
        get message room
        """
        if self.payload is None:
            raise Exception('Message payload not found ...')
        room_id = self.payload.room_id
        if room_id is None or room_id == '':
            return None
        return self.wechaty.Room.load(room_id)

    def text(self) -> str:
        """
        get message text
        """
        if self.payload is None:
            raise Exception('Message payload not found ...')
        if self.payload.text is None:
            return ''
        return self.payload.text

    async def to_recalled(self) -> Message:
        """
        Get the recalled message
        """
        if self.message_type() != MessageType.MESSAGE_TYPE_RECALLED:
            raise Exception(
                'Can not call toRecalled() on message which is not'
                ' recalled type.')

        origin_message_id = self.text()
        if origin_message_id is None:
            raise Exception('Can not find recalled message')

        log.info('get recall message <%s>', origin_message_id)
        try:
            message = self.wechaty.Message.load(origin_message_id)
            await message.ready()
            return message
        except Exception as exception:
            error_info = 'can"t load or ready message payload {}'.format(
                str(exception.args)
            )

            log.error(error_info)
            raise Exception(error_info)

    async def recall(self) -> bool:
        """
        Recall a message.
        """
        log.info('Message recall')
        success = await self.puppet.message_recall(self.message_id)
        return success

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
        user_id = self.wechaty.contact_id
        talker = self.talker()
        if talker is None:
            return False
        return talker.contact_id == user_id

    async def mention_list(self) -> List[Contact]:
        """
        Get message mentioned contactList.
        :return:
        """
        log.info('Message mention_list')
        room = self.room()
        if self.type() != MessageType.MESSAGE_TYPE_TEXT or room is None:
            return []

        # Use mention list if mention list is available
        # otherwise, process the message and get the mention list

        if self.payload is not None and self.payload.mention_ids is not None:
            async def id_to_contact(contact_id) -> Contact:
                contact = self.wechaty.Contact.load(contact_id)
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

        # const textWithoutMention = mentionNameList.reduce((prev, cur) => {
        #     const escapedCur = escapeRegExp(cur)
        #     const regex = new RegExp(`@${escapedCur}(\u2005|\u0020|$)`)
        #     return prev.replace(regex, '')
        # }, text)

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
        self_id = self.wechaty.contact_id

        # check and ready for message payload
        await self.ready()

        # check by mention_ids not mention_list
        if self.payload is None or self.payload.mention_ids is None:
            return False
        return self_id in self.payload.mention_ids

    async def ready(self):
        """
        sync load message
        """
        log.debug('Message ready <%s>', self)
        if self.is_ready():
            return

        self._payload = await self.puppet.message_payload(self.message_id)

        if self.payload is None:
            raise Exception('payload not found')

        if self.payload.from_id.strip() != '':
            talker = self.wechaty.Contact.load(self.payload.from_id)
            await talker.ready()
        if self.payload.room_id.strip() != '':
            room = self.wechaty.Room.load(self.payload.room_id)
            await room.ready()
        if self.payload.to_id.strip() != '':
            to_contact = self.wechaty.Contact.load(self.payload.to_id)
            await to_contact.ready()

    def is_ready(self) -> bool:
        """
        check message is ready
        """
        return self.payload is not None

    async def forward(self, to: Union[Room, Contact]):
        """
        doc
        :param to:
        :return:
        """
        log.info('forward() <%s>', to)
        if to is None:
            raise Exception('to param not found')
        try:
            if isinstance(to, Room):
                to_id = to.room_id
            elif isinstance(to, Contact):
                to_id = to.contact_id
            else:
                raise Exception(
                    'expected type is <Room, Contact>, but get <%s>'
                    % to.__class__)
            print(to_id)
            await self.puppet.message_forward(to_id, self.message_id)

        # pylint:disable=W0703
        except Exception as exception:
            log.error(
                'Message forward error <%s>',
                exception.args
            )
            raise exception

    def date(self) -> datetime:
        """
        Message sent date
        :return:
        """
        if self.payload is None:
            raise Exception('payload not found')

        time = datetime.fromtimestamp(self.payload.time_stamp)
        return time

    def age(self) -> int:
        """
        Returns the message age in seconds.
        :return:
        """
        if self.payload is None:
            raise Exception('Message payload not found')
        return (datetime.now() - self.date()).seconds // 1000

    async def to_file_box(self) -> FileBox:
        """
        Extract the Media File from the Message, and put it into the FileBox.
        """
        log.info('Message to FileBox')
        if self.type() == MessageType.MESSAGE_TYPE_TEXT:
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
        if self.type() != MessageType.MESSAGE_TYPE_IMAGE:
            raise Exception(
                'current message type: %s, not image type'
                % self.type()
            )
        return self.wechaty.Image.create(self.message_id)

    async def to_contact(self) -> Contact:
        """
        Get Share Card of the Message
        Extract the Contact Card from the Message, and encapsulate it into
         Contact class
        :return:
        """
        log.info('Message to Contact')
        if self.type() != MessageType.MESSAGE_TYPE_CONTACT:
            raise Exception(
                'current message type: %s, not contact type'
                % self.type()
            )

        contact_id = await self.puppet.message_contact(self.message_id)

        contact = self.wechaty.Contact.load(contact_id)
        await contact.ready()
        return contact

    async def to_url_link(self) -> UrlLink:
        """
        get url_link from message
        :return:
        """
        log.info('Message to UrlLink')
        if self.type() != MessageType.MESSAGE_TYPE_URL:
            raise Exception(
                'current message type: %s, not url type'
                % self.type()
            )
        payload = await self.puppet.message_url(self.message_id)
        if payload is None:
            raise Exception(
                'can not get url_link_payload by message: %s'
                % self.message_id)
        return UrlLink(payload)

    async def to_mini_program(self) -> MiniProgram:
        """
        get message mini_program
        :return:
        """
        log.info('Message to MiniProgram <%s>', self.message_id)

        if self.payload is None:
            raise Exception('payload not found')

        if self.type() != MessageType.MESSAGE_TYPE_MINI_PROGRAM:
            raise Exception('not a mini_program type message')

        payload = await self.puppet.message_mini_program(
            self.message_id)
        if payload is None:
            raise Exception(
                'no miniProgram payload for message %s'
                % self.message_id
            )
        return MiniProgram(payload)
