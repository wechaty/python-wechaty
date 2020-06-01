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
from abc import abstractmethod, ABCMeta
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Dict, Union,
    OrderedDict as PluginDict,
    Any)
from datetime import datetime
from copy import deepcopy
from dataclasses import dataclass
from collections import defaultdict, OrderedDict
from wechaty_puppet import get_logger, EventMessagePayload

if TYPE_CHECKING:
    from wechaty_puppet import (
        EventErrorPayload,
        EventHeartbeatPayload,
        EventReadyPayload
    )
    from wechaty.user.room_invitation import RoomInvitation
    from wechaty import (
        Wechaty,
        Room,
        Friendship,
        Contact,
        Message,
        ScanStatus
    )


log = get_logger(__name__)


@dataclass
class WechatyPluginOptions:
    metadata: dict = defaultdict


class WechatyPlugin(metaclass=ABCMeta):
    """
    abstract wechaty plugin base class

    listen events from

    """
    def __init__(self):
        self.output = {}
        self.bot: Optional[Wechaty] = None

    async def init_plugin(self, wechaty: Wechaty):
        self.bot = wechaty

    @property
    @abstractmethod
    def name(self) -> str:
        """you must give a name for wechaty plugin"""
        raise NotImplementedError

    @staticmethod
    def get_dependency_plugins() -> list[str]:
        """
        get dependency plugins
        """
        return []

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

    def get_output(self) -> dict:
        """if necessary , get the output of the plugin"""
        final_output = deepcopy(self.output)
        self.output = {}

        return final_output


PluginTree = Dict[str, Union[str, List[str]]]


class WechatyPluginManager:

    def __init__(self, wechaty: Wechaty):
        self._plugins: PluginDict[str, WechatyPlugin] = OrderedDict()
        self._wechaty: Wechaty = wechaty
        # plugins can be a topological graph pattern, this feature is not
        # supported now.
        self._dependency_tree: PluginTree = defaultdict()

    def add_plugin(self, plugin: WechatyPlugin):
        """add plugin to the manager, if the plugin name exist, it will not to
        be installed"""
        if plugin.name in self._plugins:
            log.warning(f'plugin : {plugin.name} has exist')
            return
        self._plugins[plugin.name] = plugin

    def remove_plugin(self, name: str):
        """remove plugin"""
        if name not in self._plugins:
            raise IndexError(f'plugin {name} not exist')
        self._plugins.pop(name)

    async def init_plugins(self):
        log.info('init the plugins ...')
        for name, plugin in self._plugins.items():
            log.info(f'init {name}-plugin ...')
            await plugin.init_plugin(self._wechaty)

    async def emit_events(self, event_name: str, *args, **kwargs):
        """

        during the try-stage, only support message_events

        event_name: get event
        event_payload:
        """
        if event_name == 'message':
            from wechaty import Message
            if len(args) ==1 and isinstance(args[0], Message):
                msg: Message = args[0]
            elif 'msg' in kwargs and isinstance(kwargs['msg'], Message):
                msg: Message = kwargs['msg']
            else:
                raise ValueError(f'can"t find the message params')

            for name, plugin in self._plugins.items():
                log.info(f'emit {name}-plugin ...')
                await plugin.on_message(msg)
