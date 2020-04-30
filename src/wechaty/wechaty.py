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
#
# Python 3.7: PEP 563: Postponed Evaluation of Annotations
#   https://docs.python.org/3.7/whatsnew/3.7.html#pep-563-postponed-evaluation-of-annotations
from __future__ import annotations

import asyncio
from typing import (
    # TypeVar,
    # cast,
    Optional,
    Type,
    # Union,
)
import logging
import requests
from grpclib.client import Channel
from pyee import AsyncIOEventEmitter
from wechaty_puppet import Puppet
from chatie_grpc.wechaty import (
    EventType,
    PuppetStub,
)
from .payload import (
    ScanPayload,
    MessagePayload,
    LoginPayload)
from .utils import (
    qr_terminal
)

from .user import (
    Contact,
    Friendship,
    Message,
    Tag,
    Room,
    Image,
    RoomInvitation
)

log = logging.getLogger('Wechaty')
log.setLevel(logging.INFO)


# pylint: disable=R0903
class WechatyOptions:
    """
    WechatyOptions instance
    """
    def __init__(self, puppet: Puppet, name: str = None):
        """
        WechatyOptions constructor
        """
        self.name: Optional[str] = name
        self.puppet: Puppet = puppet


class Wechaty:
    """
    docstring
    """

    _global_instance: Optional['Wechaty'] = None

    # define the event

    # save login user contact_id
    contact_id: str

    def __init__(self, token: str):
        """
        docstring
        """
        log.info('__init__()')
        self.Tag = Tag
        self.Contact = Contact
        self.Friendship = Friendship
        self.Message = Message
        self.Room = Room
        self.Image = Image
        self.RoomInvitation = RoomInvitation

        self.started: bool = False
        self.puppet: Optional[PuppetStub] = None
        self.channel: Optional[Channel] = None

        self.token = token

        self.event_stream: AsyncIOEventEmitter = AsyncIOEventEmitter()
        self._name: Optional[str] = None

    def __str__(self):
        return 'Wechaty<{0}, {1}>'.format(self.name(), self.contact_id)

    @classmethod
    def instance(cls: Type[Wechaty], token: str) -> Wechaty:
        """
        get or create global wechaty instance
        :return:
        """
        log.info('instance()')

        if cls._global_instance is None:
            cls._global_instance = cls(token=token)

        # Huan(202003): how to remove cast?
        return cls._global_instance
        # return cast(Wechaty, cls._global_instance)
        # return cls._global_instance

    def name(self) -> str:
        """name"""
        if self._name is None:
            return 'default_puppet'
        return self._name

    def on(self, event: str, listener) -> Wechaty:
        """
        listen event for puppet
        """
        self.event_stream.on(event, listener)
        return self

    async def start(self):
        """
        start the wechaty
        :return:
        """
        log.info('wechaty is starting ...')

        if self.started:
            log.info('wechaty has started ...')
            return

        await self.init_puppet()

        await self.puppet.start()
        self.started = True

        # await self.puppet.ding(data="haha")

        # async for response in self.puppet.event():
        #     if response is not None:
        #         print(response)

        # await self._listen_for_event()
        # await asyncio.sleep(1)

        while True:
            print("heart beat ...")
            await self._listen_for_event()
            # await asyncio.sleep(1)

        # def run_bot():
        #     async def bot_interval():
        #         while True:
        #             print("heart beat ...")
        #             await self._listen_for_event()
        #             await asyncio.sleep(1)
        #     asyncio.run(bot_interval())
        # thread = threading.Thread(target=run_bot, name="thread_bot")
        # thread.run()

    async def _listen_for_event(self):
        """
        listen event from hostie with heartbeat
        """
        async for response in self.puppet.event():
            if response is not None:

                if response.type == EventType.EVENT_TYPE_SCAN:
                    # create qr_code
                    payload = ScanPayload(response.payload)
                    qr_terminal(payload.qrcode)
                    self.event_stream.emit("scan", payload)

                elif response.type == EventType.EVENT_TYPE_DONG:
                    self.event_stream.emit("dong")

                elif response.type == EventType.EVENT_TYPE_MESSAGE:
                    payload = MessagePayload(response.payload)
                    message = Message.load(payload.message_id)
                    await message.ready()
                    self.event_stream.emit("message", message)

                elif response.type == EventType.EVENT_TYPE_LOGIN:
                    payload = LoginPayload.from_json(response.payload)
                    self.contact_id = payload.contact_id
                    log.info('has logined <%s>', self)

    def add_listener_function(self, event: str, listener):
        """add listener function to event emitter"""
        self.event_stream.on(event, listener)

    async def init_puppet(self):
        """
        init puppet grpc connection
        """
        response = requests.get(
            f'https://api.chatie.io/v0/hosties/{self.token}'
        )
        if response.status_code != 200:
            raise Exception("hostie server is invalid ... ")

        data = response.json()
        if 'ip' not in data or data['ip'] == '0.0.0.0':
            raise Exception('can\'t find hostie server address')

        channel = Channel(host=data["ip"], port=8788)
        self.puppet = PuppetStub(channel)
        self.channel = channel
        await self.puppet.stop()

        self.Message.set_puppet(self.puppet)
        self.Room.set_puppet(self.puppet)
        self.RoomInvitation.set_puppet(self.puppet)
        self.Contact.set_puppet(self.puppet)

        self.Message.set_wechaty(self)
        self.Room.set_wechaty(self)
        self.RoomInvitation.set_wechaty(self)
        self.Contact.set_wechaty(self)

    def set_puppet(self):
        """
        set puppet to the Room/Message/Tag class
        :return:
        """
        self.Message.set_puppet(self.puppet)

    async def stop(self):
        """
        stop the wechaty
        """
        log.info('wechaty is stoping ...')
        await self.puppet.stop()
        await self.channel.close()
