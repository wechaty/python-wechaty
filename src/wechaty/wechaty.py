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
import threading
import logging
from datetime import datetime
from typing import (
    # TypeVar,
    # cast,
    Optional,
    Type,
    # Union,
    Callable, List)
from pyee import AsyncIOEventEmitter    # type: ignore

from wechaty_puppet import (
    Puppet,
    EventLoginPayload,
    EventLogoutPayload,
    EventDongPayload,
    EventScanPayload,
    EventErrorPayload,
    EventHeartbeatPayload,
    EventFriendshipPayload,
    EventMessagePayload,
    EventRoomInvitePayload,
    EventRoomTopicPayload,
    EventRoomLeavePayload,
    EventRoomJoinPayload
)
from wechaty_puppet.schemas.event import ScanStatus
from wechaty_puppet.schemas.puppet import PUPPET_EVENT_DICT
from wechaty_puppet.state_switch import StateSwitch
from wechaty_puppet.watch_dog import WatchdogFood, Watchdog
from .user import (
    Contact,
    Friendship,
    Message,
    Tag,
    Room,
    Image,
    RoomInvitation
)
from .utils import (
    qr_terminal
)

log = logging.getLogger('Wechaty')
log.setLevel(logging.INFO)

DEFAULT_TIMEOUT = 60


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


# pylint:disable=R0902,R0904
class Wechaty:
    """
    docstring
    """

    _global_instance: Optional['Wechaty'] = None

    # define the event

    # save login user contact_id
    contact_id: str

    def __init__(self, puppet: Puppet):
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
        self.puppet: Puppet = puppet

        self.event_stream: AsyncIOEventEmitter = AsyncIOEventEmitter()
        self._name: Optional[str] = None

        self.state = StateSwitch()
        self._ready_state = StateSwitch()

        self._watchdog = Watchdog(DEFAULT_TIMEOUT)

    def __str__(self):
        return 'Wechaty<{0}, {1}>'.format(self.name(), self.contact_id)

    @classmethod
    def instance(cls: Type[Wechaty], puppet: Puppet) -> Wechaty:
        """
        get or create global wechaty instance
        :return:
        """
        log.info('instance()')

        if cls._global_instance is None:
            cls._global_instance = cls(puppet)

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

    def emit(self, event_name: str, *args, **kwargs):
        """
        emit a specific event
        """
        self.event_stream.emit(event_name, *args, **kwargs)

    def on_dong(self, listener: Callable[[str], None]) -> Wechaty:
        """
        listen dong event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('dong', listener)
        return self

    def on_error(self, listener: Callable[[str], None]) -> Wechaty:
        """
        listen error event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('error', listener)

        return self

    def on_heartbeat(self, listener: Callable[[str], None]) -> Wechaty:
        """
        listen heartbeat event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('heartbeat', listener)

        return self

    def on_friendship(self, listener: Callable[[Friendship], None]) -> Wechaty:
        """
        listen friendship event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('friendship', listener)
        return self

    def on_login(self, listener: Callable[[Contact], None]) -> Wechaty:
        """
        listen login event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('login', listener)
        return self

    def on_logout(self, listener: Callable[[str], None]) -> Wechaty:
        """
        listen logout event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('logout', listener)
        return self

    def on_message(self, listener: Callable[[Message], None]) -> Wechaty:
        """
        listen message event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('message', listener)
        return self

    def on_ready(self, listener: Callable[[None], None]) -> Wechaty:
        """
        listen ready event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('ready', listener)
        return self

    def on_room_invite(self, listener: Callable[[RoomInvitation], None]
                       ) -> Wechaty:
        """
        listen room_invitation event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('room_invite', listener)
        return self

    def on_room_join(self,
                     listener: Callable[[Room, List[Contact],
                                         Contact, datetime], None]) -> Wechaty:
        """
        listen room_join event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('room_join', listener)
        return self

    def on_room_leave(self, listener: Callable[[Room, List[Contact], Contact,
                                                datetime], None]) -> Wechaty:
        """
        listen room_leave event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('room_leave', listener)
        return self

    def on_room_topic(self, listener: Callable[[Room, str, str, Contact,
                                                datetime], None]) -> Wechaty:
        """
        listen room_topic event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('room_topic', listener)
        return self

    def on_scan(self, listener: Callable[[str, ScanStatus, str], None]
                ) -> Wechaty:
        """
        listen scan event for puppet

        this is friendly for code typing
        """
        self.event_stream.on('scan', listener)
        return self

    async def start(self):
        """
        start wechaty bot
        :return:
        """
        await self.init_puppet()
        await self.init_puppet_event_bridge(self.puppet)

        async def start_watchdog():
            async def dog_food() -> bool:
                try:
                    await self.puppet.ding('ding')
                    return True
                except Exception as exception:
                    log.info('can"t send ding to the bot')
                return False

            food = WatchdogFood(timeout=3)

            async def reset_bot(food, time):
                await self.stop()
                await self.start()

            async def ask_for_food(last_food, last_feed):
                log.info('dog ask for food ...')
                await self.puppet.ding()

            self._watchdog.on('sleep', ask_for_food)
            self._watchdog.feed(food)
            while True:
                log.info('bot tick <%s>', datetime.now())
                await self._watchdog.sleep()
                is_death = self._watchdog.starved_to_death()
                if is_death:
                    await self.restart()
                    break

        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(start_watchdog(), loop)
        log.info('starting ...')
        await self.puppet.start()

    async def restart(self):
        """restart the wechaty bot"""
        log.info('restarting the bot ...')
        # await self.puppet.stop()
        # await self.puppet.start()
        await self.start()

    # pylint: disable=R0912,R0915,R0914
    async def init_puppet_event_bridge(self, puppet: Puppet):
        """
        init puppet event stream
        """
        log.info('init_puppet_event_brideg() <%s>', puppet)
        event_names = PUPPET_EVENT_DICT.keys()
        for event_name in event_names:
            if event_name == 'dong':
                def dong_listener(payload: EventDongPayload):
                    log.info('receive dong event <%s>', payload)
                    self.event_stream.emit('dong', payload.data)
                    # feed food to the dog
                    food = WatchdogFood(timeout=3)
                    self._watchdog.feed(food)

                puppet.on('dong', dong_listener)
            elif event_name == 'error':
                def error_listener(payload: EventErrorPayload):
                    log
                    self.event_stream.emit('error', payload)

                puppet.on('error', error_listener)

            elif event_name == 'heart-beat':
                def heartbeat_listener(payload: EventHeartbeatPayload):
                    self.event_stream.emit('heartbeat', payload.data)

                puppet.on('heart-beat', heartbeat_listener)

            elif event_name == 'friendship':
                async def friendship_listener(payload: EventFriendshipPayload):
                    friendship = self.Friendship.load(payload.friendship_id)
                    await friendship.ready()
                    self.event_stream.emit('friendship', payload)
                    friendship.contact().emit('friendship', friendship)

                puppet.on('friendship', friendship_listener)

            elif event_name == 'login':
                async def login_listener(payload: EventLoginPayload):
                    # TODO -> should to ContactSelf
                    log.info('login() <%s>', payload)
                    contact = self.Contact.load(payload.contact_id)
                    await contact.ready()
                    self.emit('login', Contact)

                puppet.on('login', login_listener)

            elif event_name == 'logout':
                async def logout_listener(payload: EventLogoutPayload):
                    # TODO -> should to ContactSelf
                    contact = self.Contact.load(payload.contact_id)
                    await contact.ready()
                    self.emit('logout', Contact)

                puppet.on('logout', logout_listener)

            elif event_name == 'message':
                async def message_listener(payload: EventMessagePayload):
                    msg = self.Message.load(payload.message_id)
                    await msg.ready()
                    self.emit('message', msg)

                    room = msg.room()
                    if room is not None:
                        room.emit('message', room)

                puppet.on('message', message_listener)

            elif event_name == 'ready':
                def ready_listener():
                    log.info(
                        'Wechaty init_puppet_event_bridge() puppet.on(ready)')
                    self.emit('ready')
                    self._ready_state.on(True)

                puppet.on('ready', ready_listener)

            elif event_name == 'room-invite':
                async def room_invite_listener(payload: EventRoomInvitePayload):
                    invitation = self.RoomInvitation.load(
                        payload.room_invitation_id)
                    self.emit('room-invite', invitation)

                puppet.on('room-invite', room_invite_listener)

            elif event_name == 'room-join':
                async def room_join_listener(payload: EventRoomJoinPayload):
                    room = self.Room.load(payload.room_id)
                    await room.ready()

                    invitees = [self.Contact.load(invitee_id)
                                for invitee_id in payload.invited_ids]
                    for invitee in invitees:
                        await invitee.ready()

                    inviter = self.Contact.load(payload.inviter_id)
                    await inviter.ready()

                    date = datetime.fromtimestamp(payload.time_stamp)
                    self.emit('room-join', room, invitees, inviter, date)
                    room.emit('join', invitees, inviter, date)

                puppet.on('room-join', room_join_listener)

            elif event_name == 'room-leave':
                async def room_leave_listener(payload: EventRoomLeavePayload):
                    room = self.Room.load(payload.room_id)
                    # room info is dirty now
                    await room.ready(force_sync=True)

                    leavers = [self.Contact.load(inviter_id) for inviter_id
                               in payload.removed_ids]

                    for leaver in leavers:
                        await leaver.ready()

                    remover = self.Contact.load(payload.remover_id)
                    await remover.ready()

                    date = datetime.fromtimestamp(payload.time_stamp)

                    self.emit('room-leave', room, leavers, remover, date)
                    room.emit('leave', leavers, remover, date)

                    if self.puppet.self_id() in payload.removed_ids:
                        pass
                        # await self.puppet.room_payload(payload.room_id)
                        # await self.puppet.room_member_payload_dirty(
                        #     payload.room_id)

                puppet.on('room-leave', room_leave_listener)

            elif event_name == 'room-topic':
                async def room_topic_listener(payload: EventRoomTopicPayload):
                    room = self.Room.load(payload.room_id)
                    await room.ready()

                    changer = self.Contact.load(payload.changer_id)
                    await changer.ready()

                    date = datetime.fromtimestamp(payload.time_stamp)

                    self.emit('room-topic', room, payload.new_topic,
                              payload.old_topic, changer, date)
                    room.emit('topic', payload.new_topic, payload.old_topic,
                              changer, date)

                puppet.on('room-topic', room_topic_listener)

            elif event_name == 'scan':
                async def scan_listener(payload: EventScanPayload):
                    qr_code = '' if payload.qr_code is None \
                        else payload.qr_code
                    if payload.status == ScanStatus.Waiting:
                        qr_terminal(qr_code)
                    self.emit('scan', qr_code, payload.status, payload.data)

                puppet.on('scan', scan_listener)

            elif event_name == 'reset':
                pass
            else:
                raise ValueError(f'event_name <{event_name}> unsupported!')

            log.info('initPuppetEventBridge() puppet.on(%s) (listenerCount:%s) '
                     'registering...',
                     event_name, puppet.listener_count(event_name))

    def add_listener_function(self, event: str, listener):
        """add listener function to event emitter"""
        self.event_stream.on(event, listener)

    async def init_puppet(self):
        """
        init puppet grpc connection
        """

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
