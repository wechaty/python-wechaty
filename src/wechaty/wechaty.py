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
from datetime import datetime
from dataclasses import dataclass
from typing import (
    # TypeVar,
    # cast,
    Optional,
    Type,
    # Union,
    List, Union)
from pyee import AsyncIOEventEmitter    # type: ignore

from wechaty_puppet import (  # type: ignore
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
    EventRoomJoinPayload,

    ScanStatus,
    EventReadyPayload,

    get_logger
)
from wechaty_puppet.schemas.puppet import PUPPET_EVENT_DICT, PuppetOptions  # type: ignore
from wechaty_puppet.state_switch import StateSwitch     # type: ignore
from wechaty_puppet.watch_dog import WatchdogFood, Watchdog     # type: ignore
from .user import (
    Contact,
    Friendship,
    Message,
    Tag,
    Room,
    Image,
    RoomInvitation,
    MiniProgram,
    Favorite
)
from .utils import (
    qr_terminal
)

log = get_logger('Wechaty')

DEFAULT_TIMEOUT = 300


PuppetModuleName = str


@dataclass
class WechatyOptions:
    """
    WechatyOptions instance
    """
    name: Optional[str] = None
    puppet: Optional[Union[PuppetModuleName, Puppet]] = None
    puppet_options: Optional[PuppetOptions] = None


# pylint:disable=R0902,R0904
class Wechaty(AsyncIOEventEmitter):
    """
    docstring
    """

    _global_instance: Optional['Wechaty'] = None

    # define the event

    # save login user contact_id
    contact_id: str

    def __init__(self, options: Optional[WechatyOptions] = None):
        """
        docstring
        """
        super().__init__()

        if options is None:
            options = WechatyOptions(puppet='wechaty-puppet-hostie')
        if options.puppet_options is None:
            options.puppet_options = PuppetOptions()

        self.Tag = Tag
        self.Contact = Contact
        self.Friendship = Friendship
        self.Message = Message
        self.Room = Room
        self.Image = Image
        self.RoomInvitation = RoomInvitation
        self.Favorite = Favorite
        self.MiniProgram = MiniProgram
        # TODO -> url-link, miniprogram

        self.started: bool = False

        self.puppet: Puppet = self._load_puppet(options)

        self._name: Optional[str] = None

        self.state = StateSwitch()
        self._ready_state = StateSwitch()

        self._watchdog = Watchdog(DEFAULT_TIMEOUT)

    @staticmethod
    def _load_puppet(options: WechatyOptions) -> Puppet:
        """
        dynamic load puppet
        :param options:
        :return:
        """
        if options.puppet is None:
            raise Exception('puppet not exist')

        if isinstance(options.puppet, Puppet):
            return options.puppet

        if isinstance(options.puppet, PuppetModuleName):
            if options.puppet != 'wechaty-puppet-hostie':
                raise TypeError('Python Wechaty only supports wechaty-puppet-hostie right now.'
                                'This puppet is not supported: ' + options.puppet)

            #
            # wechaty-puppet-hostie
            #
            hostie_module = __import__('wechaty_puppet_hostie')
            if not hasattr(hostie_module, 'HostiePuppet'):
                raise Exception('HostiePuppet not exist in '
                                'wechaty-puppet-hostie')

            hostie_puppet_class = getattr(hostie_module, 'HostiePuppet')
            if not issubclass(hostie_puppet_class, Puppet):
                raise TypeError(f'Type {hostie_puppet_class} '
                                f'is not correct')

            return hostie_puppet_class(options.puppet_options)

        raise TypeError('puppet expected type is [Puppet, '
                        'PuppetModuleName(str)]')

    def __str__(self):
        """str format of the Room object"""
        return 'Wechaty<{0}, {1}>'.format(self.name, self.contact_id)

    @classmethod
    def instance(cls: Type[Wechaty], options: Optional[WechatyOptions] = None
                 ) -> Wechaty:
        """
        get or create global wechaty instance
        :return:
        """
        log.info('instance()')

        if cls._global_instance is None:
            cls._global_instance = cls(options)

        # Huan(202003): how to remove cast?
        return cls._global_instance
        # return cast(Wechaty, cls._global_instance)
        # return cls._global_instance

    @property
    def name(self) -> str:
        """name"""
        if self._name is None:
            return 'default_puppet'
        return self._name

    def on(self, event, f=None) -> Wechaty:
        """
        listen wechaty event
        :param event:
        :param f:
        :return:
        """
        log.info('on() listen event <%s> with <%s>', event, f)
        super().on(event, f)
        return self

    def emit(self, event, *args, **kwargs):
        """
        emit wechaty event
        :param event:
        :param args:
        :param kwargs:
        :return:
        """
        log.debug('emit() event <%s> <%s>',
                  [str(item) for item in args],
                  kwargs)
        super().emit(event, *args, **kwargs)

    async def on_error(self, payload: EventErrorPayload):
        """
        listen error event for puppet

        this is friendly for code typing
        """

    async def on_heartbeat(self, payload: EventHeartbeatPayload):
        """
        listen heartbeat event for puppet

        this is friendly for code typing
        """

    async def on_friendship(self, friendship: Friendship):
        """
        listen friendship event for puppet

        this is friendly for code typing
        """

    async def on_login(self, contact: Contact):
        """
        listen login event for puppet

        this is friendly for code typing
        """

    async def on_logout(self, contact: Contact):
        """
        listen logout event for puppet

        this is friendly for code typing
        """

    async def on_message(self, msg: Message):
        """
        listen message event for puppet

        this is friendly for code typing
        """

    async def on_ready(self, payload: EventReadyPayload):
        """
        listen ready event for puppet

        this is friendly for code typing
        """

    async def on_room_invite(self, room_invitation: RoomInvitation):
        """
        listen room_invitation event for puppet

        this is friendly for code typing
        """

    async def on_room_join(self, room: Room, invitees: List[Contact],
                           inviter: Contact, date: datetime):
        """
        listen room_join event for puppet

        this is friendly for code typing
        """

    async def on_room_leave(self, room: Room, leavers: List[Contact],
                            remover: Contact, date: datetime):
        """
        listen room_leave event for puppet

        room, leavers, remover, date

        this is friendly for code typing
        """

    async def on_room_topic(self, room: Room, new_topic: str, old_topic: str,
                            changer: Contact, date: datetime):
        """
        listen room_topic event for puppet

        this is friendly for code typing
        """

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        """
        listen scan event for puppet

        this is friendly for code typing
        """

    async def start(self):
        """
        start wechaty bot
        :return:
        """
        await self.init_puppet()
        await self.init_puppet_event_bridge(self.puppet)

        async def start_watchdog():

            food = WatchdogFood(timeout=3)

            async def ask_for_food(last_food, last_feed):
                log.debug('dog ask for food <%s> <%s> ...',
                          last_food, last_feed)
                await self.puppet.ding()

            self._watchdog.on('sleep', ask_for_food)
            self._watchdog.feed(food)
            while True:
                log.debug('bot tick <%s>', datetime.now())
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
        log.info('init_puppet_event_bridge() <%s>', puppet)
        event_names = PUPPET_EVENT_DICT.keys()
        for event_name in event_names:
            if event_name == 'dong':
                def dong_listener(payload: EventDongPayload):
                    log.debug('receive <dong> event <%s>', payload)
                    self.emit('dong', payload.data)
                    # feed food to the dog
                    food = WatchdogFood(timeout=30)
                    self._watchdog.feed(food)

                puppet.on('dong', dong_listener)
            elif event_name == 'error':
                async def error_listener(payload: EventErrorPayload):
                    log.info('receive <error> event <%s>', payload)
                    self.emit('error', payload)
                    await self.on_error(payload)

                puppet.on('error', error_listener)

            elif event_name == 'heart-beat':
                async def heartbeat_listener(payload: EventHeartbeatPayload):
                    log.info('receive <heart-beat> event <%s>', payload)
                    self.emit('heartbeat', payload.data)
                    await self.on_heartbeat(payload)

                puppet.on('heart-beat', heartbeat_listener)

            elif event_name == 'friendship':
                async def friendship_listener(payload: EventFriendshipPayload):
                    log.info('receive <friendship> event <%s>', payload)
                    friendship = self.Friendship.load(payload.friendship_id)
                    await friendship.ready()
                    self.emit('friendship', friendship)
                    friendship.contact().emit('friendship', friendship)
                    await self.on_friendship(friendship)

                puppet.on('friendship', friendship_listener)

            elif event_name == 'login':
                async def login_listener(payload: EventLoginPayload):
                    # set login contact_id
                    self.contact_id = payload.contact_id
                    log.info('receive <login> event <%s>', payload)
                    contact = self.Contact.load(payload.contact_id)
                    await contact.ready()
                    self.emit('login', Contact)
                    await self.on_login(contact)

                puppet.on('login', login_listener)

            elif event_name == 'logout':
                async def logout_listener(payload: EventLogoutPayload):
                    # TODO -> should to ContactSelf
                    log.info('receive <logout> event <%s>', payload)
                    contact = self.Contact.load(payload.contact_id)
                    await contact.ready()
                    self.emit('logout', Contact)
                    await self.on_logout(contact)

                puppet.on('logout', logout_listener)

            elif event_name == 'message':
                async def message_listener(payload: EventMessagePayload):
                    log.debug('receive <message> event <%s>', payload)
                    msg = self.Message.load(payload.message_id)
                    await msg.ready()
                    log.info('receive message <%s>', msg)
                    self.emit('message', msg)
                    await self.on_message(msg)

                    room = msg.room()
                    if room is not None:
                        room.emit('message', room)

                puppet.on('message', message_listener)

            elif event_name == 'ready':
                async def ready_listener(payload: EventReadyPayload):
                    log.info('receive <ready> event <%s>')
                    self.emit('ready', payload)
                    self._ready_state.on(True)
                    await self.on_ready(payload)

                puppet.on('ready', ready_listener)

            elif event_name == 'room-invite':
                async def room_invite_listener(payload: EventRoomInvitePayload):
                    log.info('receive <room-invite> event <%s>')
                    invitation = self.RoomInvitation.load(
                        payload.room_invitation_id)
                    self.emit('room-invite', invitation)
                    await self.on_room_invite(invitation)

                puppet.on('room-invite', room_invite_listener)

            elif event_name == 'room-join':
                async def room_join_listener(payload: EventRoomJoinPayload):
                    log.info('receive <room-join> event <%s>')
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
                    await self.on_room_join(room, invitees, inviter, date)

                    room.emit('join', invitees, inviter, date)

                puppet.on('room-join', room_join_listener)

            elif event_name == 'room-leave':
                async def room_leave_listener(payload: EventRoomLeavePayload):
                    log.info('receive <room-leave> event <%s>')
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
                    await self.on_room_leave(room, leavers, remover, date)

                    room.emit('leave', leavers, remover, date)

                    if self.puppet.self_id() in payload.removed_ids:
                        pass
                        # await self.puppet.room_payload(payload.room_id)
                        # await self.puppet.room_member_payload_dirty(
                        #     payload.room_id)

                puppet.on('room-leave', room_leave_listener)

            elif event_name == 'room-topic':
                async def room_topic_listener(payload: EventRoomTopicPayload):
                    log.info('receive <room-topic> event <%s>')
                    room = self.Room.load(payload.room_id)
                    await room.ready()

                    changer = self.Contact.load(payload.changer_id)
                    await changer.ready()

                    date = datetime.fromtimestamp(payload.time_stamp)

                    self.emit('room-topic', room, payload.new_topic,
                              payload.old_topic, changer, date)

                    await self.on_room_topic(room, payload.new_topic,
                                             payload.old_topic, changer, date)

                    room.emit('topic', payload.new_topic, payload.old_topic,
                              changer, date)

                puppet.on('room-topic', room_topic_listener)

            elif event_name == 'scan':
                async def scan_listener(payload: EventScanPayload):
                    log.info('receive <scan> event <%s>')
                    qr_code = '' if payload.qrcode is None \
                        else payload.qrcode
                    if payload.status == ScanStatus.Waiting:
                        qr_terminal(qr_code)
                    self.emit('scan', payload.status, qr_code,  payload.data)
                    await self.on_scan(payload.status, qr_code,  payload.data)

                puppet.on('scan', scan_listener)

            elif event_name == 'reset':
                log.info('receive <reset> event <%s>')
            else:
                raise ValueError(f'event_name <{event_name}> unsupported!')

            log.info('initPuppetEventBridge() puppet.on(%s) (listenerCount:%s) '
                     'registering...',
                     event_name, puppet.listener_count(event_name))

    def add_listener_function(self, event: str, listener):
        """add listener function to event emitter"""
        self.on(event, listener)

    async def init_puppet(self):
        """
        init puppet grpc connection
        """

        self.Message.set_puppet(self.puppet)
        self.Room.set_puppet(self.puppet)
        self.RoomInvitation.set_puppet(self.puppet)
        self.Contact.set_puppet(self.puppet)
        self.Friendship.set_puppet(self.puppet)
        self.Image.set_puppet(self.puppet)
        self.Tag.set_puppet(self.puppet)

        self.Message.set_wechaty(self)
        self.Room.set_wechaty(self)
        self.RoomInvitation.set_wechaty(self)
        self.Contact.set_wechaty(self)
        self.Friendship.set_wechaty(self)
        self.Image.set_wechaty(self)
        self.Tag.set_wechaty(self)

    async def stop(self):
        """
        stop the wechaty
        """
        log.info('wechaty is stoping ...')
        await self.puppet.stop()
