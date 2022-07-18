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
import logging
import sys
import traceback
from datetime import datetime
from dataclasses import dataclass
from typing import (
    # TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Optional,
    Type,
    List,
    Union,
    cast,
)
import signal

import requests.exceptions
from grpclib.exceptions import StreamTerminatedError
from pyee import AsyncIOEventEmitter
from apscheduler.schedulers.base import BaseScheduler

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
    EventRoomJoinPayload,

    ScanStatus,
    EventReadyPayload,

    WechatyPuppetError,

    get_logger,
)
from wechaty_puppet.schemas.puppet import PUPPET_EVENT_DICT, PuppetOptions
from wechaty_puppet.state_switch import StateSwitch

from wechaty.user.url_link import UrlLink
from wechaty.utils.async_helper import SingleIdContainer

from wechaty.user import (
    Contact,
    Friendship,
    Message,
    Tag,
    Room,
    Image,
    RoomInvitation,
    MiniProgram,
    Favorite,
    ContactSelf
)

from wechaty.plugin import (
    WechatyPlugin,
    WechatyPluginManager,
    WechatySchedulerOptions
)

from wechaty.exceptions import (
    WechatyStatusError,
    WechatyConfigurationError,
    WechatyOperationError,
)

from wechaty.utils import timestamp_to_date, qr_terminal


log: logging.Logger = get_logger('Wechaty')

DEFAULT_TIMEOUT = 300

PuppetModuleName = str


async def get_shutdown_trigger() -> Callable[[], Coroutine[Any, Any, Any]]:
    """register the system shutdown trigger event"""
    signal_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    def _signal_handler(*_: Any) -> None:  # noqa: N803
        print('receive signal event ...')
        signal_event.set()

    for signal_name in ["SIGINT", "SIGTERM", "SIGBREAK"]:
        if hasattr(signal, signal_name):
            try:
                loop.add_signal_handler(getattr(signal, signal_name), _signal_handler)
            except NotImplementedError:
                # Add signal handler may not be implemented on Windows
                signal.signal(getattr(signal, signal_name), _signal_handler)

    return signal_event.wait


async def shutdown(trigger: Callable[[], Coroutine[Any, Any, Any]]) -> None:
    """when trigger the shutdown, it will call sys.exit"""
    await trigger()
    sys.exit(0)


# pylint: disable=too-many-instance-attributes
@dataclass
class WechatyOptions:
    """
    WechatyOptions instance
    """
    name: str = 'Python Wechaty'
    puppet: Union[PuppetModuleName, Puppet] = 'wechaty-puppet-service'
    puppet_options: PuppetOptions = PuppetOptions()

    host: str = '0.0.0.0'
    port: int = 5000

    # expose the puppet options at here to make it easy to user
    token: Optional[str] = None
    endpoint: Optional[str] = None

    scheduler: Optional[Union[WechatySchedulerOptions, BaseScheduler]] = None


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

        # 1. int the puppet options
        if options is None:
            options = WechatyOptions(puppet='wechaty-puppet-service')

        if options.puppet_options is None:
            options.puppet_options = PuppetOptions()

        options.puppet_options.token = options.puppet_options.token or options.token
        options.puppet_options.end_point = options.puppet_options.end_point or options.endpoint
        options.puppet = self._load_puppet(options)

        # 2. init the scheduler options
        self._options = options

        # pylint: disable=C0103
        self.Tag: Type[Tag] = Tag
        # pylint: disable=C0103
        self.Contact: Type[Contact] = Contact
        # pylint: disable=C0103
        self.ContactSelf: Type[ContactSelf] = ContactSelf
        # pylint: disable=C0103
        self.Friendship: Type[Friendship] = Friendship
        # pylint: disable=C0103
        self.Message: Type[Message] = Message
        # pylint: disable=C0103
        self.Room: Type[Room] = Room
        # pylint: disable=C0103
        self.Image: Type[Image] = Image
        # pylint: disable=C0103
        self.RoomInvitation: Type[RoomInvitation] = RoomInvitation
        self.Favorite: Type[Favorite] = Favorite
        self.MiniProgram: Type[MiniProgram] = MiniProgram
        self.UrlLink: Type[UrlLink] = UrlLink
        # TODO -> url-link, miniprogram

        self.started: bool = False

        self._name: Optional[str] = None

        self.state = StateSwitch()
        self._ready_state = StateSwitch()

        self._puppet: Puppet = options.puppet
        self._plugin_manager: WechatyPluginManager = WechatyPluginManager(
            self,
            (options.host, options.port)
        )

    @property
    def puppet(self) -> Puppet:
        """
        Always expected to return a non-null puppet instance, or raise an error.
        :return:
        """
        if not self._puppet:
            raise WechatyStatusError('Wechaty puppet not loaded!')
        return self._puppet

    @staticmethod
    def _load_puppet(options: WechatyOptions) -> Puppet:
        """
        dynamic load puppet
        :param options:
        :return:
        """
        if options.puppet is None:
            raise WechatyConfigurationError('puppet not exist')

        if isinstance(options.puppet, Puppet):
            return options.puppet

        if isinstance(options.puppet, PuppetModuleName):
            if options.puppet != 'wechaty-puppet-service':
                raise TypeError('Python Wechaty only supports wechaty-puppet-service right now.'
                                'This puppet is not supported: ' + options.puppet)

            #
            # wechaty-puppet-service
            #
            puppet_service_module = __import__('wechaty_puppet_service')
            if not hasattr(puppet_service_module, 'PuppetService'):
                raise WechatyConfigurationError('PuppetService not exist in '
                                                'wechaty-puppet-service')

            puppet_service_class = getattr(puppet_service_module, 'PuppetService')
            if not issubclass(puppet_service_class, Puppet):
                raise WechatyConfigurationError(f'Type {puppet_service_class} '
                                                f'is not correct')

            return puppet_service_class(options.puppet_options)

        raise WechatyConfigurationError('puppet expected type is [Puppet, '
                                        'PuppetModuleName(str)]')

    def __str__(self) -> str:
        """str format of the Room object"""
        return f'Wechaty<{self.name}, {self.contact_id}>'

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

    def use(self, plugin: Union[WechatyPlugin, List[WechatyPlugin]]) -> Wechaty:
        """register the plugin"""
        if isinstance(plugin, WechatyPlugin):
            plugins = [plugin]
        else:
            plugins = plugin
        for item in plugins:
            self._plugin_manager.add_plugin(item)
        return self

    @property
    def name(self) -> str:
        """name"""
        if self._name is None:
            return 'default_puppet'
        return self._name

    def on(self, event: str, f: Callable[..., Any] = None) -> Wechaty:
        """
        listen wechaty event
        :param event:
        :param f:
        :return:
        """
        log.info('on() listen event <%s> with <%s>', event, f)
        super().on(event, f)
        return self

    def emit(self, event: str, *args: Any, **kwargs: Any) -> bool:
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
        return super().emit(event, *args, **kwargs)

    async def on_error(self, payload: EventErrorPayload) -> None:
        """
        listen error event for puppet

        this is friendly for code typing
        """

    async def on_heartbeat(self, payload: EventHeartbeatPayload) -> None:
        """
        listen heartbeat event for puppet

        this is friendly for code typing
        """

    async def on_friendship(self, friendship: Friendship) -> None:
        """
        listen friendship event for puppet

        this is friendly for code typing
        """

    async def on_login(self, contact: Contact) -> None:
        """
        listen login event for puppet

        this is friendly for code typing
        """

    async def on_logout(self, contact: Contact) -> None:
        """
        listen logout event for puppet

        this is friendly for code typing
        """

    async def on_message(self, msg: Message) -> None:
        """
        listen message event for puppet

        this is friendly for code typing
        """

    async def on_ready(self, payload: EventReadyPayload) -> None:
        """
        listen ready event for puppet

        this is friendly for code typing
        """

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        """
        listen room_invitation event for puppet

        this is friendly for code typing
        """

    async def on_room_join(self, room: Room, invitees: List[Contact],
                           inviter: Contact, date: datetime) -> None:
        """
        listen room_join event for puppet

        this is friendly for code typing
        """

    async def on_room_leave(self, room: Room, leavers: List[Contact],
                            remover: Contact, date: datetime) -> None:
        """
        listen room_leave event for puppet

        room, leavers, remover, date

        this is friendly for code typing
        """

    async def on_room_topic(self, room: Room, new_topic: str, old_topic: str,
                            changer: Contact, date: datetime) -> None:
        """
        listen room_topic event for puppet

        this is friendly for code typing
        """

    async def on_scan(self, qr_code: str, status: ScanStatus,
                      data: Optional[str] = None) -> None:
        """
        listen scan event for puppet

        this is friendly for code typing
        """

    async def start(self) -> None:
        """
        start wechaty bot
        :return:
        """

        # If the network is shut-down, we should catch the connection
        # error and restart after a minute.
        try:

            await self.init_puppet()
            await self.init_puppet_event_bridge(self.puppet)

            log.info('starting puppet ...')
            await self.puppet.start()

            self.started = True

            # register the system signal

        except (requests.exceptions.ConnectionError, StreamTerminatedError, OSError):

            # TODO: this problem is the most common error, so I add chinese & detail info for
            #  developer. this should be removed later.
            # pylint: disable=C0301
            error_info = '''The network is not good, the bot will try to restart after 60 seconds.
But here are some suggestions for you:
* 查看token是否可用？（过期或协议不可用）
* docker 服务是否正常启动？
* python-wechaty bot 是否正常启动？
* python-wechaty bot 是否能ping通docker服务？
* 由于版本细节问题，目前python-wechaty 支持最好的wechaty镜像为：[wechaty/wechaty:0.65](https://hub.docker.com/layers/wechaty/wechaty/0.65/images/sha256-d39b9fb5dece3a8ffa88b80a8ccfd916be14b9d0de72115732c3ee714b0d6a96?context=explore)

I suggest that you should follow the template code from: https://wechaty.readthedocs.io/zh_CN/latest/ to avoid the unnecessary bugs.
'''
            log.error(error_info)
            await asyncio.sleep(60)
            await self.restart()

        except WechatyPuppetError:
            traceback.print_exc()
            loop = asyncio.get_event_loop()
            loop.stop()

        except Exception as e:      # pylint: disable=broad-except
            print(e)

    async def restart(self) -> None:
        """restart the wechaty bot"""
        log.info('restarting the bot ...')
        await self.stop()
        await self.start()

    # pylint: disable=R0912,R0915,R0914
    async def init_puppet_event_bridge(self, puppet: Puppet) -> None:
        """
        init puppet event stream
        """
        log.info('init_puppet_event_bridge() <%s>', puppet)
        event_names = PUPPET_EVENT_DICT.keys()

        # prevent once time event to emit twice and more ...
        once_event = set()

        for event_name in event_names:
            if event_name == 'dong':
                def dong_listener(payload: EventDongPayload) -> None:
                    log.debug('receive <dong> event <%s>', payload)
                    self.emit('dong', payload.data)

                puppet.on('dong', dong_listener)
            elif event_name == 'error':
                async def error_listener(payload: EventErrorPayload) -> None:
                    if isinstance(payload, EventErrorPayload):
                        log.info('receive <error> event <%s>', payload)
                        self.emit('error', payload)
                        await self.on_error(payload)
                    else:
                        # Fixme: there is always <error> event, which the reason is not clear
                        # if there is no valid error message, it should not throw the error
                        if not payload:
                            return
                        log.error('internal error <%s>', payload)

                puppet.on('error', error_listener)

            elif event_name == 'heart-beat':
                async def heartbeat_listener(payload: EventHeartbeatPayload) -> None:
                    log.info('receive <heart-beat> event <%s>', payload)
                    self.emit('heartbeat', payload.data)
                    await self.on_heartbeat(payload)

                puppet.on('heart-beat', heartbeat_listener)

            elif event_name == 'friendship':
                async def friendship_listener(payload: EventFriendshipPayload) -> None:
                    log.info('receive <friendship> event <%s>', payload)
                    friendship = self.Friendship.load(payload.friendship_id)
                    await friendship.ready()
                    self.emit('friendship', friendship)

                    # this method will cause _events error, refer to
                    # :https://github.com/wechaty/python-wechaty/issues/122
                    # and this feature is considering to be removed, refer to
                    # https://github.com/wechaty/python-wechaty/issues/127

                    # friendship.contact().emit('friendship', friendship)
                    await self.on_friendship(friendship)

                    await self._plugin_manager.emit_events(
                        'friendship', friendship
                    )

                puppet.on('friendship', friendship_listener)

            elif event_name == 'login':
                async def login_listener(payload: EventLoginPayload) -> None:
                    if 'login' in once_event:
                        return
                    once_event.add('login')

                    # init the plugins
                    await self._plugin_manager.start()

                    # set login contact_id
                    self.contact_id = payload.contact_id
                    log.info('receive <login> event <%s>', payload)
                    contact = self.ContactSelf.load(payload.contact_id)
                    await contact.ready()
                    self.emit('login', contact)
                    await self.on_login(contact)

                    # emit the login event to plugins
                    await self._plugin_manager.emit_events('login', contact)

                puppet.on('login', login_listener)

            elif event_name == 'logout':
                async def logout_listener(payload: EventLogoutPayload) -> None:
                    # TODO -> should to ContactSelf
                    log.info('receive <logout> event <%s>', payload)
                    contact = self.ContactSelf.load(payload.contact_id)
                    await contact.ready()
                    self.emit('logout', contact)
                    await self.on_logout(contact)

                    # emit the logout event to plugins
                    await self._plugin_manager.emit_events('logout', contact)

                puppet.on('logout', logout_listener)

            elif event_name == 'message':
                async def message_listener(payload: EventMessagePayload) -> None:
                    # sometimes, it will receive the specific message with two/three times
                    if SingleIdContainer.instance().exist(payload.message_id):
                        return

                    log.debug('receive <message> event <%s>', payload)
                    msg = self.Message.load(payload.message_id)
                    await msg.ready()
                    log.info('receive message <%s>', msg)
                    self.emit('message', msg)
                    await self.on_message(msg)

                    room = msg.room()
                    if room is not None:
                        room.emit('message', room)

                    # emit the message event to plugins
                    await self._plugin_manager.emit_events('message', msg)

                puppet.on('message', message_listener)

            elif event_name == 'ready':
                async def ready_listener(payload: EventReadyPayload) -> None:
                    if 'ready' in once_event:
                        return
                    once_event.add('ready')

                    log.info('receive <ready> event <%s>', payload)
                    self.emit('ready', payload)
                    self._ready_state.on(True)
                    await self.on_ready(payload)

                puppet.on('ready', ready_listener)

            elif event_name == 'room-invite':
                async def room_invite_listener(payload: EventRoomInvitePayload) -> None:
                    log.info('receive <room-invite> event <%s>', payload)
                    invitation = self.RoomInvitation.load(
                        payload.room_invitation_id)
                    self.emit('room-invite', invitation)
                    await self.on_room_invite(invitation)

                    # emit the room-invite event to plugins
                    await self._plugin_manager.emit_events(
                        'room-invite',
                        invitation
                    )

                puppet.on('room-invite', room_invite_listener)

            elif event_name == 'room-join':
                async def room_join_listener(payload: EventRoomJoinPayload) -> None:
                    log.info('receive <room-join> event <%s>', payload)
                    room = self.Room.load(payload.room_id)
                    await room.ready()

                    invitees = [self.Contact.load(invitee_id)
                                for invitee_id in payload.invited_ids]
                    for invitee in invitees:
                        await invitee.ready()

                    inviter = self.Contact.load(payload.inviter_id)
                    await inviter.ready()

                    # timestamp is from hostie-server, but the value range is
                    # 10^10 ~ 10^13
                    # refer to
                    # :https://github.com/wechaty/python-wechaty/issues/1290
                    date = timestamp_to_date(payload.timestamp)

                    self.emit('room-join', room, invitees, inviter, date)
                    await self.on_room_join(room, invitees, inviter, date)

                    room.emit('join', invitees, inviter, date)

                    # emit the room-join event to plugins
                    await self._plugin_manager.emit_events(
                        'room-join', room,
                        invitees, inviter, date
                    )

                puppet.on('room-join', room_join_listener)

            elif event_name == 'room-leave':
                async def room_leave_listener(payload: EventRoomLeavePayload) -> None:
                    log.info('receive <room-leave> event <%s>', payload)
                    room = self.Room.load(payload.room_id)
                    # room info is dirty now
                    await room.ready(force_sync=True)

                    leavers = [self.Contact.load(inviter_id) for inviter_id
                               in payload.removed_ids]

                    for leaver in leavers:
                        await leaver.ready()

                    remover = self.Contact.load(payload.remover_id)
                    await remover.ready()

                    date = timestamp_to_date(payload.timestamp)

                    self.emit('room-leave', room, leavers, remover, date)
                    await self.on_room_leave(room, leavers, remover, date)

                    room.emit('leave', leavers, remover, date)

                    if self.puppet.self_id() in payload.removed_ids:
                        pass
                        # await self.puppet.room_payload(payload.room_id)
                        # await self.puppet.room_member_payload_dirty(
                        #     payload.room_id)

                    # emit the room-leave event to plugins
                    await self._plugin_manager.emit_events(
                        'room-leave', room, leavers, remover, date
                    )

                puppet.on('room-leave', room_leave_listener)

            elif event_name == 'room-topic':
                async def room_topic_listener(payload: EventRoomTopicPayload) -> None:
                    log.info('receive <room-topic> event <%s>', payload)

                    room: Room = self.Room.load(payload.room_id)
                    await room.ready()

                    changer = self.Contact.load(payload.changer_id)
                    await changer.ready()

                    date = timestamp_to_date(payload.timestamp)

                    self.emit('room-topic', room, payload.new_topic,
                              payload.old_topic, changer, date)

                    await self.on_room_topic(room, payload.new_topic,
                                             payload.old_topic, changer, date)

                    room.emit('topic', payload.new_topic, payload.old_topic,
                              changer, date)

                    # emit the room-topic to plugins
                    await self._plugin_manager.emit_events(
                        'room-topic', room,
                        payload.new_topic,
                        payload.old_topic,
                        changer, date
                    )

                puppet.on('room-topic', room_topic_listener)

            elif event_name == 'scan':
                async def scan_listener(payload: EventScanPayload) -> None:
                    log.info('receive <scan> event <%s>', payload)
                    qr_code = '' if payload.qrcode is None \
                        else payload.qrcode
                    if payload.status == ScanStatus.Waiting:
                        qr_terminal(qr_code)
                        log.info(
                            'or you can scan qrcode from: '
                            'https://wechaty.js.org/qrcode/%s',
                            qr_code
                        )
                    self.emit('scan', qr_code, payload.status, payload.data)
                    await self.on_scan(qr_code, payload.status, payload.data)

                    # emit the scan event to plugins
                    await self._plugin_manager.emit_events(
                        'scan', qr_code,
                        payload.status,
                        payload.data
                    )

                puppet.on('scan', scan_listener)

            elif event_name == 'reset':
                log.info('receive <reset> event <%s>')
            else:
                raise WechatyOperationError(f'event_name <{event_name}> unsupported!')

            log.info('initPuppetEventBridge() puppet.on(%s) (listenerCount:%s) '
                     'registering...',
                     event_name, puppet.listener_count(event_name))

    def add_listener_function(self, event: str, listener: Callable[..., Any]) -> None:
        """add listener function to event emitter"""
        self.on(event, listener)

    async def init_puppet(self) -> None:
        """
        init puppet grpc connection
        """
        # Recreate puppet instance
        self._puppet = self._load_puppet(self._options)

        # Using metaclass to create a dynamic subclass to server multi bot instances.
        meta_info = dict(_puppet=self.puppet, _wechaty=self, abstract=False)
        self.Contact = type('Contact', (Contact,), meta_info)
        self.ContactSelf = type('ContactSelf', (ContactSelf,), meta_info)
        self.Favorite = type('Favorite', (Favorite,), meta_info)
        self.Friendship = type('Friendship', (Friendship,), meta_info)
        self.Image = type('Image', (Image,), meta_info)
        self.Message = type('Message', (Message,), meta_info)
        self.MiniProgram = type('MiniProgram', (MiniProgram,), meta_info)
        self.UrlLink = type('UrlLink', (UrlLink,), meta_info)
        self.Room = type('Room', (Room,), meta_info)
        self.RoomInvitation = type('RoomInvitation', (RoomInvitation,), meta_info)
        self.Tag = type('Tag', (Tag,), meta_info)

    async def stop(self) -> None:
        """
        stop the wechaty
        """
        log.info('wechaty is stopping ...')
        await self.puppet.stop()
        self.started = False

        self._puppet = None
        log.info('wechaty has been stopped gracefully!')

    def user_self(self) -> ContactSelf:
        """
        get user self
        :return:
        """
        user_id = self.puppet.self_id()
        user = self.ContactSelf.load(user_id)
        # cast Contact -> ContactSelf
        user = cast(ContactSelf, user)
        return user

    def self(self) -> ContactSelf:
        """
        get user self
        :return: user_self
        """
        return self.user_self()
