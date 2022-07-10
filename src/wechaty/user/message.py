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

import dataclasses
import json
import re

from typing import (
    Optional,
    Union,
    List
)

from datetime import datetime
from wechaty_puppet import (
    FileBox,
    MessagePayload,
    MessageQueryFilter,
    MessageType,
    get_logger
)

from wechaty.exceptions import WechatyPayloadError, WechatyOperationError
from wechaty.user.contact_self import ContactSelf
from wechaty.utils import timestamp_to_date

from ..accessory import Accessory
from .mini_program import MiniProgram
# TODO -> remove Sayable interface temporary
# from ..types import Sayable

from .contact import Contact
from .url_link import UrlLink
from .image import Image
from .room import Room


log = get_logger('Message')

SUPPORTED_MESSAGE_FILE_TYPES: List[MessageType] = [
    MessageType.MESSAGE_TYPE_ATTACHMENT,
    MessageType.MESSAGE_TYPE_EMOTICON,
    MessageType.MESSAGE_TYPE_IMAGE,
    MessageType.MESSAGE_TYPE_VIDEO,
    MessageType.MESSAGE_TYPE_AUDIO
]


# pylint: disable=R0904,R0903
class Message(Accessory[MessagePayload]):
    """
    接受和发送的消息都封装成Message对象。

    All of wechaty messages will be encapsulated as a Message object.

    you can get all of message attribute through publish method.
    """

    Type = MessageType

    def __init__(self, message_id: str):
        """
        the initialization for Message object which only receive the
        message_id data to fetch payload.
        """
        super().__init__()

        self.message_id = message_id

    def message_type(self) -> MessageType:
        """
        get the message type
        for more details, please refer to : https://github.com/wechaty/grpc/blob/master/proto/wechaty/puppet/message.proto#L9
        """
        return self.payload.type

    def __str__(self) -> str:
        """
        format string for message, which keep consistant with wechaty/wechaty

        refer to : https://github.com/wechaty/wechaty/blob/master/src/user/message.ts#L195
        """
        if not self.is_ready():
            return f'Message <{self.message_id}> is not ready'

        message_list = [
            'Message',
            f'#{self.message_type().name.lower()}',
            # talker can't be None
            f'[🗣 {self.talker()}',
        ]
        if self.room():
            message_list.append(f'@👥 {self.room()}]')

        if self.message_type() == MessageType.MESSAGE_TYPE_TEXT:
            message_list.append(f'\t{self.text()[:70]}')

        return ''.join(message_list)

    async def say(self, msg: Union[str, Contact, FileBox, UrlLink, MiniProgram],
                  mention_ids: Optional[List[str]] = None) -> Optional[Message]:
        """
        send the message to the conversation envrioment which is source of this message.

        If this message is from room, so you can send message to this room.

        If this message is from contact, so you can send message to this contact, not to room.

        向联系人或群聊发送一段文字, 名片, 媒体文件或者链接.

        > 注意: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

        Args:
            msg: the message object which can be type of str/Contact/FileBox/UrlLink/MiniProgram
            mention_ids: you can send message with `@person`, the only things you should do is to
                set contact_id to mention_ids.
        Examples:
            >>> message.say('hello')
            >>> message.say(Contact('contact_id'))
            >>> message.say(FileBox('file_path'))
            >>> message.say(UrlLink('url'))
            >>> message.say(MiniProgram('app_id'))

            ```python
            import asyncio
            from wechaty import Wechaty, Message
            from wechaty import Wechaty, Contact, FileBox, UrlLink
            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    text = msg.text()
                    # 1. 发送文字到联系人
                    if text == "叮":
                        await msg.say('咚')
                        return
                    # 2. 发送媒体文件到联系人
                    if text == "媒体":
                        file_box1 = FileBox.from_url('https://wechaty.github.io/wechaty/images/bot-qr-code.png', "bot-qr-code.png")
                        file_box2 = FileBox.from_file('text.txt', "text.txt")
                        await msg.say(file_box1)
                        await msg.say(file_box2)
                        return
                    # 3. 发送名片到联系人
                    if text == "名片":
                        contact_card = self.Contact.load('lijiarui')  # 把`lijiarui`更改为您在微信中的任意联系人的姓名
                        await msg.say(contact_card)
                        return
                    # 4. 发送链接到联系人
                    if text == "链接":
                        url_link = UrlLink.create(
                            description='WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
                            thumbnail_url='https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
                            title='Welcome to Wechaty',
                            url='https://github.com/wechaty/wechaty',
                        )
                        await msg.say(url_link)
                        return
                    # 5. 发送小程序 (暂时只有`wechaty-puppet-macpro`支持该服务)
                    if text == "小程序":
                        miniProgram = self.MiniProgram.create_from_json({
                            "appid": 'gh_0aa444a25adc',
                            "title": '我正在使用Authing认证身份，你也来试试吧',
                            "pagePath": 'routes/explore.html',
                            "description": '身份管家',
                            "thumbUrl": '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
                            "thumbKey": '42f8609e62817ae45cf7d8fefb532e83',
                        })
                        await msg.say(miniProgram)
                        return
            asyncio.run(MyBot().start())
            ```
        Returns:
            Optional[Message]: if the message is sent successfully, return the message object.
        """
        log.info('say() <%s>', msg)

        if not msg:
            log.error('can"t say nothing')
            return None

        room = self.room()
        if room is not None:
            conversation_id = room.room_id
        else:
            talker = self.talker()
            if talker is None:
                raise WechatyPayloadError('Message must be from room/contact')
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
                conversation_id=conversation_id,
                contact_id=msg.contact_id,
            )
        elif isinstance(msg, FileBox):
            message_id = await self.puppet.message_send_file(
                conversation_id=conversation_id, file=msg)
        elif isinstance(msg, UrlLink):
            message_id = await self.puppet.message_send_url(
                conversation_id=conversation_id, url=json.dumps(dataclasses.asdict(msg.payload)))
        elif isinstance(msg, MiniProgram):
            assert msg.payload is not None
            message_id = await self.puppet.message_send_mini_program(
                conversation_id=conversation_id,
                mini_program=msg.payload)
        else:
            raise WechatyPayloadError('message type should be str, '
                                      'Contact/FileBox/UrlLink/MiniProgram')

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
        """find the message from the server.

        Args:
            talker_id (Optional[str], optional): the id of talker.
            message_id (Optional[str], optional): the id of message.
            room_id (Optional[str], optional): the id of room.
            text (Optional[str], optional): you can search message by sub-string of the text.
            to_id (Optional[str], optional): the id of receiver.
            message_type (Optional[MessageType], optional): the type of the message

        Returns:
            Optional[Message]: if find the messages, return the first of it.
                               if can't find message, return None
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
        """find the message from the server.

        Args:
            talker_id (Optional[str], optional): the id of talker.
            message_id (Optional[str], optional): the id of message.
            room_id (Optional[str], optional): the id of room.
            text (Optional[str], optional): you can search message by sub-string of the text.
            to_id (Optional[str], optional): the id of receiver.
            message_type (Optional[MessageType], optional): the type of the message

        Returns:
            List[Message]: return all of the searched messages
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
        """get the talker of the message

        获取消息的发送者。
        Args:
            None
        Examples:
            ```python
            import asyncio
            from wechaty import Wechaty, Message
            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    print(msg.talker())
            asyncio.run(MyBot().start())
            ```
        Raises:
            WechatyPayloadError: can't find the talker information from the payload

        Returns:
            Contact: the talker contact object
        """
        talker_id = self.payload.from_id
        if talker_id is None:
            raise WechatyPayloadError('message must be from Contact')
        return self.wechaty.Contact.load(talker_id)

    def to(self) -> Optional[Contact]:
        """get the receiver, which is the Contact type, of the message

        获取消息的接收者, 如果消息是在群聊发出的Message.to()会返回None, 请使用 Message.room() 获取群聊对象。
        Args:
            None
        Examples:
            ```python
            import asyncio
            from wechaty import Wechaty, Message, Contact
            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    talker: Contact = msg.talker()
                    text: str = msg.text()
                    to_contact = msg.to()
                    if to_contact:
                        name = to_contact.name
                        print(f"接收者: {name} 联系人: {talker.name} 内容: {text}")
                    else:
                        print(f"联系人: {talker.name} 内容: {text}")
            asyncio.run(MyBot().start())
            ```
        Returns:
            Optional[Contact]: if the message is private to contact, return the contact object
                else return None
        """
        to_id = self.payload.to_id
        if to_id is None:
            return None
        return self.wechaty.Contact.load(to_id)

    def room(self) -> Optional[Room]:
        """get the room from the messge

        获取消息来自的群聊. 如果消息不是来自群聊, 则返回None.
        Args:
            None
        Examples:
            >>> msg.room()

            ```python
                import asyncio
                from wechaty import Wechaty, Message, Contact

                class MyBot(Wechaty):
                
                    async def on_message(self, msg: Message) -> None:
                        talker: Contact = msg.talker()
                        text: str = msg.text()
                        room = msg.room()
                        if room:
                            room_name = await room.topic()
                            print(f"群聊名: {room_name} 联系人(消息发送者): {talker.name} 内容: {text}")
                        else:
                            print(f"联系人: {talker.name} 内容: {text}")
                asyncio.run(MyBot().start())
            ```
        Returns:
            Optional[Room]: if the message is from room, return the contact object.
                else return .
        """
        room_id = self.payload.room_id
        if room_id is None or room_id == '':
            return None
        return self.wechaty.Room.load(room_id)

    def chatter(self) -> Union[Room, Contact]:
        """return the chat container object of the message. If the message is from room,
        return the Room object. else return Contact object

        Returns:
            Optional[Room, Contact]: return the room/contact object
        """
        room: Optional[Room] = self.room()
        if room:
            return room
        talker: Contact = self.talker()
        return talker

    def text(self) -> str:
        """
        get message text

        获取对话的消息文本.
        Args:
            None
        Examples:
            ```python
            import asyncio
            from wechaty import Wechaty, Message, Contact

            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    talker: Contact = msg.talker()
                    text: str = msg.text()
                    room = msg.room()
                    if room:
                        room_name = await room.topic()
                        print(f"群聊名: {room_name} 联系人(消息发送者): {talker.name} 内容: {text}")
                    else:
                        print(f"联系人: {talker.name} 内容: {text}")

            asyncio.run(MyBot().start())
            ```
        Raises:
            WechatyPayloadError: can't find the text from the payload
        Returns:
            str: the message text
        """
        if self.payload.text:
            return self.payload.text
        return ''

    async def to_recalled(self) -> Message:
        """
        Get the recalled message

        获取撤回的信息的文本
        Args:
            None
        Examples:
            ```python
                import asyncio
                from wechaty import Wechaty, Message
                from wechaty_puppet import MessageType
                class MyBot(Wechaty):
                
                    async def on_message(self, msg: Message) -> None:
                        if msg.type() == MessageType.MESSAGE_TYPE_RECALLED:
                            recalled_message = await msg.to_recalled()
                            print(f"{recalled_message}被撤回")
                asyncio.run(MyBot().start())
            ```
        Returns:
            Message: the recalled message
        """
        if self.message_type() != MessageType.MESSAGE_TYPE_RECALLED:
            raise WechatyOperationError(
                'Can not call toRecalled() on message which is not'
                ' recalled type.')

        origin_message_id = self.text()
        if origin_message_id is None:
            raise WechatyPayloadError('Can not find recalled message')

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
            raise WechatyOperationError(error_info)

    async def recall(self) -> bool:
        """
        Recall a message.

        撤回这条信息
        Args:
            None
        Example:
            ```python
            >>> msg.recall()
            ```
        Returns:
            bool: True if recall success, else False
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

        获取消息的类型
        Notes:
            注意: `MessageType`是枚举类型; <br/>
            `from wechaty_puppet import MessageType`

            * MessageType.MESSAGE_TYPE_UNSPECIFIED
            * MessageType.MESSAGE_TYPE_ATTACHMENT
            * MessageType.MESSAGE_TYPE_AUDIO
            * MessageType.MESSAGE_TYPE_CONTACT
            * MessageType.MESSAGE_TYPE_EMOTICON
            * MessageType.MESSAGE_TYPE_IMAGE
            * MessageType.MESSAGE_TYPE_TEXT
            * MessageType.MESSAGE_TYPE_VIDEO
            * MessageType.MESSAGE_TYPE_CHAT_HISTORY
            * MessageType.MESSAGE_TYPE_LOCATION
            * MessageType.MESSAGE_TYPE_MINI_PROGRAM 
            * MessageType.MESSAGE_TYPE_TRANSFER 
            * MessageType.MESSAGE_TYPE_RED_ENVELOPE 
            * MessageType.MESSAGE_TYPE_RECALLED 
            * MessageType.MESSAGE_TYPE_URL 

        Args:
            None
        Examples:
            ```python
            >>> msg.type()
            ```
            ```python
            import asyncio
            from wechaty import Wechaty, Message
            from wechaty_puppet import MessageType

            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    if msg.type() == MessageType.MESSAGE_TYPE_TEXT:
                        print(f"这是个文本消息")

            asyncio.run(MyBot().start())
            ```
        Returns:
            MessageType: the message type
        """
        return self.payload.type

    def is_self(self) -> bool:
        """
        Check if a message is sent by self

        检查这个消息是否是由自己发出的

        Args:
            None
        Examples:
            ```python
            import asyncio
            from wechaty import Wechaty, Message
            from wechaty_puppet import MessageType

            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    if msg.is_self():
                        print("这个是Bot自己发出的消息")
                    else:
                        print("这是由别人发出的消息")

            asyncio.run(MyBot().start())
            ```
        Returns:
            bool: True if message is sent by self, else False
        """
        login_user: ContactSelf = self.wechaty.user_self()
        talker = self.talker()
        if talker is None:
            return False
        return talker.contact_id == login_user.contact_id

    async def mention_list(self) -> List[Contact]:
        """
        Get message mentioned contactList.

        以列表的形式获取消息所提及(@)的人.

        Args:
            None
        Examples:
            ```python
            import asyncio
            from wechaty import Wechaty,  Message

            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    contact_mention_list = await msg.mention_list()
                    print(contact_mention_list)

            asyncio.run(MyBot().start())
            ```
        Returns:
            List[Contact]: the contact list mentioned in the message
        """
        log.info('Message mention_list')
        room = self.room()
        if self.type() != MessageType.MESSAGE_TYPE_TEXT or room is None:
            return []

        # Use mention list if mention list is available
        # otherwise, process the message and get the mention list

        if self.payload is not None and self.payload.mention_ids is not None:
            async def id_to_contact(contact_id: str) -> Contact:
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

        返回过滤掉@name后的消息
        Examples:
            ```python
            import asyncio
            from wechaty import Wechaty, Message

            class MyBot(Wechaty):
                # 原消息为 `@Gary Helloworld`
                async def on_message(self, msg: Message) -> None:
                    print(await msg.mention_text()) # 打印`Helloworld`

            asyncio.run(MyBot().start())
            ```
        Returns:
            str: the message text without mention
        """
        text = self.text()
        room = self.room()

        mention_list = await self.mention_list()

        if room is None or len(mention_list) <= 0:
            return text

        async def get_alias_or_name(member: Contact) -> str:
            if room is not None:
                alias = await room.alias(member)
                if alias:
                    return alias
            return member.name

        # TODO -> change to python async best practice
        # flake8: disable=F841
        mention_names = [
            await get_alias_or_name(member)
            for member in mention_list]

        while len(mention_names) > 0:
            escaped_cur = mention_names.pop()
            pattern = re.compile(f'@{escaped_cur}(\u2005|\u0020|$)')
            text = re.sub(pattern, '', text)

        return text

    async def mention_self(self) -> bool:
        """
        Check if a message is mention self.
        :return:
        """
        user_self: ContactSelf = self.wechaty.user_self()

        # check and ready for message payload
        await self.ready()

        # check by mention_ids not mention_list
        if self.payload is None or self.payload.mention_ids is None:
            return False
        return user_self.contact_id in self.payload.mention_ids

    async def ready(self) -> None:
        """
        sync load message
        """
        log.debug('Message ready <%s>', self)
        if self.is_ready():
            return

        self.payload = await self.puppet.message_payload(self.message_id)

        if self.payload.from_id.strip() != '':
            talker = self.wechaty.Contact.load(self.payload.from_id)
            await talker.ready()
        if self.payload.room_id.strip() != '':
            room = self.wechaty.Room.load(self.payload.room_id)
            await room.ready()
        if self.payload.to_id.strip() != '':
            to_contact = self.wechaty.Contact.load(self.payload.to_id)
            await to_contact.ready()

    async def forward(self, to: Union[Room, Contact]) -> None:
        """
        转发接收到的信息. 此操作不会触发on-message事件.
        Args:
            to: 转发到的目标对象
        Examples:
            ```python
            import asyncio
            from wechaty import Wechaty,  Message

            class MyBot(Wechaty):
            
                async def on_message(self, msg: Message) -> None:
                    room = await self.Room.find("wechaty")
                    if room:
                        await msg.forward(room)
                        print("成功转发消息到wechaty群聊")

            asyncio.run(MyBot().start())
            ```
        """
        log.info('forward() <%s>', to)
        if to is None:
            raise WechatyPayloadError('to param not found')
        try:
            if isinstance(to, Room):
                to_id = to.room_id
            elif isinstance(to, Contact):
                to_id = to.contact_id
            else:
                raise WechatyPayloadError(
                    'expected type is <Room, Contact>, but get <%s>'
                    % to.__class__)
            print(to_id)
            await self.puppet.message_forward(to_id, self.message_id)

        # pylint:disable=W0703
        except Exception as exception:
            message = 'Message forward error <%s>' % exception.args
            log.error(message)
            raise WechatyOperationError(message)

    def date(self) -> datetime:
        """
        Message sent date

        获取消息发送的时间
        Notes:
            Python2.7: https://docs.python.org/2.7/library/datetime.html#datetime.datetime

            Python3+ ：https://docs.python.org/3.7/library/datetime.html#datetime.datetime

            for datetime.fromtimestamp. It’s common for this to be restricted to years from 1970 through 2038.

            2145888000 is 2038-01-01 00:00:00 UTC for second

            2145888000 is 1970-01-26 04:04:48 UTC for millisecond
        Examples:
            举个例子, 有条消息是`8:43:01`发送的, 而当我们在Wechaty中接收到它的时候时间已经为 `8:43:15`, 那么这时 `age()`返回的值为 `8:43:15 - 8:43:01 = 14 (秒)`
        Returns:
            datetime: message sent date
        """
        if self.payload.timestamp > 2145888000:
            time = datetime.fromtimestamp(self.payload.timestamp / 1000)
        else:
            time = datetime.fromtimestamp(self.payload.timestamp)
        return timestamp_to_date(self.payload.timestamp)

    def age(self) -> int:
        """
        Returns the message age in seconds.
        :return:
        """
        return (datetime.now() - self.date()).seconds // 1000

    async def to_file_box(self) -> FileBox:
        """
        从消息中提取媒体文件，并将其封装为FileBox类返回。

        Extract the Media File from the Message, and put it into the FileBox.

        Notes:
            文件类型的消息包括:

            * MESSAGE_TYPE_ATTACHMENT
            * MESSAGE_TYPE_EMOTICON
            * MESSAGE_TYPE_IMAGE
            * MESSAGE_TYPE_VIDEO

            提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

        Examples:
            ```python
            >>> msg.to_file_box()
            ```
        Returns:
            FileBox: file box

        """
        log.info('Message to FileBox')
        if self.type() not in SUPPORTED_MESSAGE_FILE_TYPES:
            raise WechatyOperationError(
                f'this type <{self.type().name}> message can"t be converted to '
                f'FileBox'
            )
        msg_type: MessageType = self.type()
        if msg_type == MessageType.MESSAGE_TYPE_IMAGE:
            file_box = await self.puppet.message_image(self.message_id)
        else:
            file_box = await self.puppet.message_file(self.message_id)
        
        return file_box

    def to_image(self) -> Image:
        """
        从消息中提取图像文件，以便我们可以使用不同的图像大小。

        Extract the Image File from the Message, so that we can use
        different image sizes.
        Note:
            提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
        Examples:
            ```python
            >>> msg.to_image()
            ```
        Returns:
            Image: image
        """
        log.info('Message to Image() for message %s', self.message_id)
        if self.type() != MessageType.MESSAGE_TYPE_IMAGE:
            raise WechatyOperationError(
                'current message type: %s, not image type'
                % self.type()
            )
        return self.wechaty.Image.create(self.message_id)

    async def to_contact(self) -> Contact:
        """
        获取消息中的联系人卡片, 并从卡片中提取联系人将其封装到联系人类中返回

        Get Share Card of the Message
        Extract the Contact Card from the Message, and encapsulate it into
         Contact class

        Notes:
            提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
        Examples:
            ```python
            >>> msg.to_contact()
            ```
        Returns:
            Contact: contact
        """
        log.info('Message to Contact')
        if self.type() != MessageType.MESSAGE_TYPE_CONTACT:
            raise WechatyOperationError(
                'current message type: %s, not contact type'
                % self.type()
            )

        contact_id = await self.puppet.message_contact(self.message_id)

        contact = self.wechaty.Contact.load(contact_id)
        await contact.ready()
        return contact

    async def to_url_link(self) -> UrlLink:
        """
        获取消息的UrlLink, 从消息中提取UrlLink，并封装到UrlLink类中返回

        get url_link from message
        Notes:
            提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
        Examples:
            ```python
            >>> msg.to_url_link()
            ```
        Returns:
            UrlLink: url_link
        """
        log.info('Message to UrlLink')
        if self.type() != MessageType.MESSAGE_TYPE_URL:
            raise WechatyOperationError(
                'current message type: %s, not url type'
                % self.type()
            )
        payload = await self.puppet.message_url(self.message_id)
        if payload is None:
            raise WechatyPayloadError(
                'can not get url_link_payload by message: %s'
                % self.message_id)
        return self.wechaty.UrlLink(payload)

    async def to_mini_program(self) -> MiniProgram:
        """
        从消息中提取小程序卡片，并将其封装为MiniProgram类返回。

        get message mini_program

        Notes:
            提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
        Examples:
            ```python
            >>> msg.to_mini_program()
            ```
        Returns:
            MiniProgram: mini_program
        """
        log.info('Message to MiniProgram <%s>', self.message_id)

        if self.type() != MessageType.MESSAGE_TYPE_MINI_PROGRAM:
            raise WechatyOperationError('not a mini_program type message')

        payload = await self.puppet.message_mini_program(
            self.message_id)
        if payload is None:
            raise WechatyPayloadError(
                'no miniProgram payload for message %s'
                % self.message_id
            )
        return self.wechaty.MiniProgram(payload)
