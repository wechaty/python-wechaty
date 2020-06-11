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

from abc import abstractmethod, ABCMeta
from enum import Enum
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Dict,
    Union,
    Any)
import re
from datetime import datetime
from copy import deepcopy
from dataclasses import dataclass
from collections import defaultdict, OrderedDict
from wechaty_puppet import get_logger   # type: ignore

if TYPE_CHECKING:
    from wechaty_puppet import (
        EventErrorPayload,
        EventHeartbeatPayload,
        EventReadyPayload,
        ScanStatus
    )
    from wechaty import (
        Room,
        Friendship,
        Contact,
        Message,
        Wechaty
    )
    from wechaty.user.room_invitation import RoomInvitation


log = get_logger(__name__)


@dataclass
class WechatyPluginOptions:
    """options for wechaty plugin"""
    name: Optional[str] = None
    metadata: Optional[dict] = None


class PluginStatus(Enum):
    """plugin running status"""
    Running = 0
    Stopped = 1


class WechatyPlugin(metaclass=ABCMeta):
    """
    abstract wechaty plugin base class

    listen events from

    """
    def __init__(self, options: Optional[WechatyPluginOptions] = None):
        self.output: Dict[str, Any] = {}
        self.bot: Optional[Wechaty] = None
        if options is None:
            options = WechatyPluginOptions()
        self.options = options

    async def init_plugin(self, wechaty: Wechaty):
        """set wechaty to the plugin"""
        self.bot = wechaty

    @property
    @abstractmethod
    def name(self) -> str:
        """you must give a name for wechaty plugin"""
        raise NotImplementedError

    @staticmethod
    def get_dependency_plugins() -> List[str]:
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

    # pylint: disable=R0913
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
    """manage the wechaty plugin, It will support some features."""
    def __init__(self, wechaty: Wechaty):
        self._plugins: Dict[str, WechatyPlugin] = OrderedDict()
        self._wechaty: Wechaty = wechaty
        self._plugin_status: Dict[str, PluginStatus] = {}
        # plugins can be a topological graph pattern, this feature is not
        # supported now.
        self._dependency_tree: PluginTree = defaultdict()

    # pylint: disable=R1711
    @staticmethod
    def _load_plugin_from_local_file(plugin_path: str) -> Optional[WechatyPlugin]:
        """load plugin from local file"""
        log.info('load plugin from local file <%s>', plugin_path)
        return None

    # pylint: disable=R1711
    @staticmethod
    def _load_plugin_from_github_url(github_url: str
                                     ) -> Optional[WechatyPlugin]:
        """load plugin from github url, but, this is dangerous"""
        log.info('load plugin from github url <%s>', github_url)
        return None

    def add_plugin(self, plugin: Union[str, WechatyPlugin]):
        """add plugin to the manager, if the plugin name exist, it will not to
        be installed"""
        if isinstance(plugin, str):
            regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}'
                r'\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if regex.match(plugin) is None:
                # load plugin from local file
                plugin_instance = self._load_plugin_from_local_file(plugin)
            else:
                plugin_instance = self._load_plugin_from_github_url(plugin)
            if plugin_instance is None:
                raise Exception('can"t load plugin %s' % plugin)
        else:
            if plugin.name in self._plugins:
                log.warning('plugin : %s has exist', plugin.name)
                return
            plugin_instance = plugin

        self._plugins[plugin_instance.name] = plugin_instance
        # default wechaty plugin status is Running
        self._plugin_status[plugin_instance.name] = PluginStatus.Running

    def remove_plugin(self, name: str):
        """remove plugin"""
        if name not in self._plugins:
            raise IndexError(f'plugin {name} not exist')
        self._plugins.pop(name)
        self._plugin_status.pop(name)

    def _check_plugins(self, name: str):
        """
        check the plugins whether
        """
        if name not in self._plugins and name not in self._plugin_status:
            raise Exception('plugins <%s> not exist' % name)

    def stop_plugin(self, name: str):
        """stop the plugin"""
        log.info('stopping the plugin <%s>', name)
        self._check_plugins(name)

        if self._plugin_status[name] == PluginStatus.Stopped:
            log.warning('plugins <%s> is stopped', name)
        self._plugin_status[name] = PluginStatus.Stopped

    def start_plugin(self, name: str):
        """starting the plugin"""
        log.info('starting the plugin <%s>', name)
        self._check_plugins(name)
        self._plugin_status[name] = PluginStatus.Running

    def plugin_status(self, name: str) -> PluginStatus:
        """get the plugin status"""
        self._check_plugins(name)
        return self._plugin_status[name]

    async def init_plugins(self):
        """
        set wechaty to plugins
        """
        log.info('init the plugins ...')
        for name, plugin in self._plugins.items():
            log.info('init %s-plugin ...', name)
            await plugin.init_plugin(self._wechaty)

    async def emit_events(self, event_name: str, *args, **kwargs):
        """

        during the try-stage, only support message_events

        event_name: get event
        event_payload:
        """
        if event_name == 'message':
            # this is not type linting, it's needed to be imported at top-level
            # , So, it must occurs cyclic-import problems, to resolve this, a
            # simple way is that we import package at local-level.

            # pylint: disable=import-outside-toplevel
            from wechaty import Message
            if len(args) == 1 and isinstance(args[0], Message):
                msg: Message = args[0]
            elif 'msg' in kwargs and isinstance(kwargs['msg'], Message):
                msg = kwargs['msg']
            else:
                raise ValueError('can"t find the message params')

            # this will make the plugins running sequential, _plugins
            # is a sort dict
            for name, plugin in self._plugins.items():
                log.info('emit %s-plugin ...', name)
                if self.plugin_status(name) == PluginStatus.Running:
                    await plugin.on_message(msg)
