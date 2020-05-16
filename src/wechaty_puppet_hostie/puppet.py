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

import json
import logging
from typing import Optional, List, Tuple
import requests

from chatie_grpc.wechaty import (  # type: ignore
    PuppetStub,
)
# pylint: disable=E0401
from grpclib.client import Channel
# pylint: disable=E0401
from pyee import AsyncIOEventEmitter  # type: ignore

from wechaty_puppet import (
    EventScanPayload,
    EventReadyPayload,

    EventDongPayload,
    EventRoomTopicPayload,
    EventRoomLeavePayload,
    EventRoomJoinPayload,
    EventRoomInvitePayload,

    EventMessagePayload,
    EventLogoutPayload,
    EventLoginPayload,
    EventFriendshipPayload,
    EventHeartbeatPayload,
    EventErrorPayload,
    EventResetPayload,
    FileBox, RoomMemberPayload, RoomPayload, RoomInvitationPayload,
    RoomQueryFilter, FriendshipPayload, ContactPayload, MessagePayload,
    MessageQueryFilter
)
from wechaty_puppet import ImageType, EventType
from wechaty_puppet import Puppet
from wechaty_puppet.schemas.mini_program import MiniProgramPayload
from wechaty_puppet.schemas.puppet import PuppetOptions
# pylint: disable=R0904
from wechaty_puppet.schemas.url_link import UrlLinkPayload

log = logging.getLogger('HostiePuppet')


class HostiePuppet(Puppet):
    """
    grpc wechaty puppet implementation
    """

    def __init__(self, options: PuppetOptions, name: str = 'hostie_puppet'):
        super(HostiePuppet, self).__init__(options, name)
        # self.channel: Channel = None
        # self.puppet_stub: PuppetStub = None

        self.channel, self.puppet_stub = self.init_puppet()

        self._event_stream: AsyncIOEventEmitter = AsyncIOEventEmitter()

        self.init_puppet()
        # self.puppet_stub.room_member_list()

    async def room_list(self) -> List[str]:
        """
        get all room list
        :return:
        """
        response = await self.puppet_stub.room_list()
        if response is None:
            raise ValueError('can"t get room_list response')
        return response.ids

    async def message_image(self, message_id: str, image_type: ImageType
                            ) -> FileBox:
        """
        get message image data
        :param message_id:
        :param image_type:
        :return:
        """

        response = await self.puppet_stub.message_image(
            id=message_id,
            type=image_type)
        if response is None:
            # TODO -> need to refactor the raised error
            raise ValueError('response is invalid')
        return FileBox.from_base64(response.filebox)

    def on(self, event_name: str, caller):
        """
        listen event from the wechaty
        :param event_name:
        :param caller:
        :return:
        """
        # TODO -> if the event is listened twice, how to handle this problem
        self._event_stream.on(event_name, caller)

    def listener_count(self, event_name: str) -> int:
        """
        how to get event count
        :param event_name:
        :return:
        """
        listeners = self._event_stream.listeners(event_name)
        return len(listeners)

    async def contact_list(self) -> List[str]:
        """
        get contact list
        :return:
        """
        response = await self.puppet_stub.contact_list()
        if response is None:
            # TODO -> need to refactor the raised error
            raise ValueError('response is invalid')
        return response.ids

    async def tag_contact_delete(self, tag_id: str) -> None:
        """
        delete some tag
        :param tag_id:
        :return:
        """
        await self.puppet_stub.tag_contact_delete(id=tag_id)
        return None

    async def tag_favorite_delete(self, tag_id: str) -> None:
        """
        delete tag favorite
        :param tag_id:
        :return:
        """
        # chatie_grpc has not implement this function
        return None

    async def tag_contact_add(self, tag_id: str, contact_id: str):
        """
        add a tag to contact
        :param tag_id:
        :param contact_id:
        :return:
        """
        await self.puppet_stub.tag_contact_add(
            id=tag_id, contact_id=contact_id)

    async def tag_favorite_add(self, tag_id: str, contact_id: str):
        """
        add a tag to favorite
        :param tag_id:
        :param contact_id:
        :return:
        """
        # chatie_grpc has not implement this function
        return

    async def tag_contact_remove(self, tag_id: str, contact_id: str):
        """
        remove a tag from contact
        :param tag_id:
        :param contact_id:
        :return:
        """
        await self.puppet_stub.tag_contact_remove(
            id=tag_id,
            contact_id=contact_id)

    async def tag_contact_list(self, contact_id: Optional[str] = None
                               ) -> List[str]:
        """
        get tag list from a contact
        :param contact_id:
        :return:
        """
        response = await self.puppet_stub.tag_contact_list(
            contact_id=contact_id)
        return response.ids

    async def message_send_text(self, conversation_id: str, message: str,
                                mention_ids: List[str] = None) -> str:
        """
        send text message
        :param conversation_id:
        :param message:
        :param mention_ids:
        :return:
        """
        response = await self.puppet_stub.message_send_text(
            conversation_id=conversation_id,
            text=message, mentonal_ids=mention_ids)
        return response.id

    async def message_send_contact(self, contact_id: str,
                                   conversation_id: str) -> str:
        """
        send contact message
        :param contact_id:
        :param conversation_id:
        :return:
        """
        response = await self.puppet_stub.message_send_contact(
            conversation_id=conversation_id,
            contact_id=contact_id
        )
        return response.id

    async def message_send_file(self, conversation_id: str,
                                file: FileBox) -> str:
        """
        send file message
        :param conversation_id:
        :param file:
        :return:
        """
        response = await self.puppet_stub.message_send_file(
            conversation_id=conversation_id,
            filebox=file.to_json_str()
        )
        return response.id

    async def message_send_url(self, conversation_id: str, url: str) -> str:
        """
        send url message
        :param conversation_id:
        :param url:
        :return:
        """
        response = await self.puppet_stub.message_send_url(
            conversation_id=conversation_id,
            url_link=url
        )
        return response.id

    async def message_send_mini_program(self, conversation_id: str,
                                        mini_program: MiniProgramPayload
                                        ) -> str:
        """
        send mini_program message
        :param conversation_id:
        :param mini_program:
        :return:
        """
        response = await self.puppet_stub.message_send_mini_program(
            conversation_id=conversation_id,
            # TODO -> check mini_program key
            mini_program=mini_program.thumb_url
        )
        return response.id

    async def message_search(self, query: Optional[MessageQueryFilter] = None
                             ) -> List[str]:
        """
        # TODO -> this function should not be here ?
        :param query:
        :return:
        """
        return []

    async def message_recall(self, message_id: str) -> bool:
        """
        recall the message
        :param message_id:
        :return:
        """
        response = await self.puppet_stub.message_recall(id=message_id)
        return response.success

    async def message_payload(self, message_id: str) -> MessagePayload:
        """
        get message payload
        :param message_id:
        :return:
        """
        response = await self.puppet_stub.message_payload(id=message_id)
        return response

    async def message_forward(self, to_id: str, message_id: str):
        """
        forward the message
        :param to_id:
        :param message_id:
        :return:
        """
        # TODO -> we should get the type of the message, and forward the message
        # to different conversation_id
        # await self.puppet_stub.message_send_mini_program()

    async def message_file(self, message_id: str) -> FileBox:
        """
        extract file from message
        :param message_id:
        :return:
        """
        response = await self.puppet_stub.message_file(id=message_id)
        return FileBox.from_base64(response.filebox)

    async def message_contact(self, message_id: str) -> str:
        """
        extract
        :param message_id:
        :return:
        """
        response = await self.puppet_stub.message_contact(id=message_id)
        return response.id

    async def message_url(self, message_id: str) -> UrlLinkPayload:
        """
        extract url
        :param message_id:
        :return:
        """
        response = await self.puppet_stub.message_url(id=message_id)
        return UrlLinkPayload(url=response.url_link)

    async def message_mini_program(self, message_id: str) -> MiniProgramPayload:
        """
        extract mini_program from message
        :param message_id:
        :return:
        """
        # TODO -> need to MiniProgram
        # response = await self.puppet_stub.message_mini_program(id=message_id)
        # return MiniProgramPayload(response.mini_program)
        return MiniProgramPayload()

    async def contact_alias(self, contact_id: str, alias: Optional[str] = None
                            ) -> str:
        """
        get/set contact alias
        :param contact_id:
        :param alias:
        :return:
        """
        response = await self.puppet_stub.contact_alias(
            id=contact_id, alias=alias)
        if response.alias is None and alias is None:
            raise ValueError('can"t get contact<%s> alias' % contact_id)
        return response.alias

    async def contact_payload_dirty(self, contact_id: str):
        """
        # TODO this function has not been implement in chatie_grpc
        :param contact_id:
        :return:
        """

    async def contact_payload(self, contact_id: str) -> ContactPayload:
        """
        get contact payload
        :param contact_id:
        :return:
        """
        response = await self.puppet_stub.contact_payload(id=contact_id)
        return response

    async def contact_avatar(self, contact_id: str,
                             file_box: Optional[FileBox] = None) -> FileBox:
        """
        get/set contact avatar
        :param contact_id:
        :param file_box:
        :return:
        """
        response = await self.puppet_stub.contact_avatar(
            id=contact_id, filebox=file_box)
        return FileBox.from_base64(response.filebox)

    async def contact_tag_ids(self, contact_id: str) -> List[str]:
        """
        get contact tags
        :param contact_id:
        :return:
        """
        response = await self.puppet_stub.tag_contact_list(
            contact_id=contact_id)
        return response.ids

    def self_id(self) -> str:
        """
        # TODO -> how to get self_id, nwo wechaty has save login_user
            contact_id
        :return:
        """
        return ''

    async def friendship_search(self, weixin: Optional[str] = None,
                                phone: Optional[str] = None) -> Optional[str]:
        """
        search friendship by wexin/phone
        :param weixin:
        :param phone:
        :return:
        """
        if weixin is not None:
            weixin_response = await self.puppet_stub.friendship_search_weixin(
                weixin=weixin
            )
            if weixin_response is not None:
                return weixin_response.contact_id
        if phone is not None:
            phone_response = await self.puppet_stub.friendship_search_phone(
                phone=phone
            )
            if phone is not None:
                return phone_response.contact_id
        return None

    async def friendship_add(self, contact_id: str, hello: str):
        """
        try to add friendship
        :param contact_id:
        :param hello:
        :return:
        """
        await self.puppet_stub.friendship_add(
            contact_id=contact_id,
            hello=hello
        )

    async def friendship_payload(self, friendship_id: str,
                                 payload: Optional[FriendshipPayload] = None
                                 ) -> FriendshipPayload:
        """
        get/set friendship payload
        :param friendship_id:
        :param payload:
        :return:
        """
        response = await self.puppet_stub.friendship_payload(
            id=friendship_id, payload=json.dumps(payload)
        )
        return FriendshipPayload(**response.to_dict())

    async def friendship_accept(self, friendship_id: str):
        """
        accept friendship
        :param friendship_id:
        :return:
        """
        await self.puppet_stub.friendship_accept(id=friendship_id)

    async def room_create(self, contact_ids: List[str], topic: str = None
                          ) -> str:
        """
        create room
        :param contact_ids:
        :param topic:
        :return: created room_id
        """
        response = await self.puppet_stub.room_create(
            contact_ids=contact_ids,
            topic=topic
        )
        return response.id

    async def room_search(self, query: RoomQueryFilter = None) -> List[str]:
        """
        # TODO -> search function should be wechaty module
        search room
        :param query:
        :return:
        """
        return []

    async def room_invitation_payload(self,
                                      room_invitation_id: str,
                                      payload: Optional[RoomInvitationPayload]
                                      = None) -> RoomInvitationPayload:
        """
        get room_invitation_payload
        """
        response = await self.puppet_stub.room_invitation_payload(
            id=room_invitation_id,
            payload=payload
        )
        return RoomInvitationPayload(**response.to_dict())

    async def room_invitation_accept(self, room_invitation_id: str):
        """

        :param room_invitation_id:
        :return:
        """

    async def contact_self_qr_code(self) -> str:
        """

        :return:
        """
        return ''

    async def contact_self_name(self, name: str):
        """

        :param name:
        :return:
        """

    async def contact_signature(self, signature: str):
        """

        :param signature:
        :return:
        """

    async def room_validate(self, room_id: str) -> bool:
        """

        :param room_id:
        :return:
        """

    async def room_payload_dirty(self, room_id: str):
        """

        :param room_id:
        :return:
        """

    async def room_member_payload_dirty(self, room_id: str):
        """

        :param room_id:
        :return:
        """

    async def room_payload(self, room_id: str) -> RoomPayload:
        """

        :param room_id:
        :return:
        """
        response = await self.puppet_stub.room_payload(id=room_id)
        return response

    async def room_members(self, room_id: str) -> List[str]:
        """

        :param room_id:
        :return:
        """
        response = await self.puppet_stub.room_member_list(id=room_id)
        return response.member_ids

    async def room_add(self, room_id: str, contact_id: str):
        pass

    async def room_delete(self, room_id: str, contact_id: str):
        pass

    async def room_quit(self, room_id: str):
        pass

    async def room_topic(self, room_id: str, new_topic: str):
        pass

    async def room_announce(self, room_id: str,
                            announcement: str = None) -> str:
        """

        :param room_id:
        :param announcement:
        :return:
        """
        return ''

    async def room_qr_code(self, room_id: str) -> str:
        """

        :param room_id:
        :return:
        """
        return ''

    async def room_member_payload(self, room_id: str,
                                  contact_id: str) -> RoomMemberPayload:
        """

        :param room_id:
        :param contact_id:
        :return:
        """

    async def room_avatar(self, room_id: str) -> FileBox:
        pass

    def init_puppet(self) -> Tuple[Channel, PuppetStub]:
        """
        start puppet channelcontact_self_qr_code
        """
        response = requests.get(
            f'https://api.chatie.io/v0/hosties/{self.options.token}'
        )

        if response.status_code != 200:
            raise Exception('hostie server is invalid ... ')

        data = response.json()
        if 'ip' not in data or data['ip'] == '0.0.0.0':
            raise Exception("can't find hostie server address")
        log.info('init puppet hostie')
        log.debug('get puppet ip address : <%s>', data)

        channel = Channel(host=data['ip'], port=8788)
        puppet_stub = PuppetStub(channel)
        # try to restart puppet_stub
        return channel, puppet_stub

    async def start(self) -> None:
        """
        start puppet_stub
        :return:
        """
        # await self.puppet_stub.stop()
        # loop = asyncio.get_event_loop()
        # loop.run_forever()
        #
        # loop.run_until_complete(self.puppet_stub.start(), self._listen_for_event())

        # await asyncio.gather(
        #     self.puppet_stub.start(),
        #     self._listen_for_event()
        # )
        # loop = asyncio.get_running_loop()
        #
        # asyncio.run_coroutine_threadsafe(
        #     self.puppet_stub.start(),
        #     loop
        # )
        log.info('stopping the puppet ...')
        await self.puppet_stub.stop()
        log.info('starting the puppet ...')
        await self.puppet_stub.start()
        log.info('puppet has started ...')
        await self._listen_for_event()
        return None

    async def stop(self):
        """
        stop the grpc channel connection
        """

        await self.puppet_stub.stop()
        await self.channel.close()

    async def ding(self, data: Optional[str] = ''):
        """
        set the ding event
        :param data:
        :return:
        """
        log.debug('send ding info to hostie ...')
        await self.puppet_stub.ding(data=data)

    # pylint: disable=R0912,R0915
    async def _listen_for_event(self):
        """
        listen event from hostie with heartbeat
        """
        # listen event from grpclib
        log.info('listening the event from the puppet ...')
        async for response in self.puppet_stub.event():
            if response is not None:
                log.info('receive event: <%s>', response)
                payload_data: dict = json.loads(response.payload)
                if response.type == int(EventType.EVENT_TYPE_SCAN):
                    log.debug('receiving scan info <%s>', response)
                    # create qr_code
                    payload = EventScanPayload(**payload_data)
                    self._event_stream.emit('scan', payload)

                elif response.type == int(EventType.EVENT_TYPE_DONG):
                    log.debug('receiving dong info <%s>', response)
                    payload = EventDongPayload(**payload_data)
                    self._event_stream.emit('dong', payload)

                elif response.type == int(EventType.EVENT_TYPE_MESSAGE):
                    # payload = get_message_payload_from_response(response)
                    log.debug('receiving message info <%s>', response)
                    event_message_payload = EventMessagePayload(
                        message_id=payload_data['messageId'])
                    self._event_stream.emit('message', event_message_payload)

                elif response.type == int(EventType.EVENT_TYPE_HEARTBEAT):
                    log.debug('receving heartbeat info <%s>', response)
                    payload = EventHeartbeatPayload(**payload_data)
                    self._event_stream.emit('heartbeat', payload)

                elif response.type == int(EventType.EVENT_TYPE_ERROR):
                    log.info('receving error info <%s>', response)
                    payload = EventErrorPayload(**payload_data)
                    self._event_stream.emit('error', payload)

                elif response.type == int(EventType.EVENT_TYPE_FRIENDSHIP):
                    payload = EventFriendshipPayload(**payload_data)
                    self._event_stream.emit('friendship', payload)

                elif response.type == int(EventType.EVENT_TYPE_ROOM_JOIN):
                    payload = EventRoomJoinPayload(**payload_data)
                    self._event_stream.emit('room-join', payload)

                elif response.type == int(EventType.EVENT_TYPE_ROOM_INVITE):
                    payload = EventRoomInvitePayload(**payload_data)
                    self._event_stream.emit('room-invite', payload)

                elif response.type == int(EventType.EVENT_TYPE_ROOM_LEAVE):
                    payload = EventRoomLeavePayload(**payload_data)
                    self._event_stream.emit('room-leave', payload)

                elif response.type == int(EventType.EVENT_TYPE_ROOM_TOPIC):
                    payload = EventRoomTopicPayload(**payload_data)
                    self._event_stream.emit('room-topic', payload)

                elif response.type == int(EventType.EVENT_TYPE_ROOM_TOPIC):
                    payload = EventRoomTopicPayload(**payload_data)
                    self._event_stream.emit('room-topic', payload)

                elif response.type == int(EventType.EVENT_TYPE_READY):
                    payload = EventReadyPayload(**payload_data)
                    self._event_stream.emit('ready', payload)

                elif response.type == int(EventType.EVENT_TYPE_RESET):
                    payload = EventResetPayload(**payload_data)
                    self._event_stream.emit('reset', payload)

                elif response.type == int(EventType.EVENT_TYPE_LOGIN):
                    event_login_payload = EventLoginPayload(
                        contact_id=payload_data['contactId'])
                    self._event_stream.emit('login', event_login_payload)

                elif response.type == int(EventType.EVENT_TYPE_LOGOUT):
                    payload = EventLogoutPayload(
                        contact_id=payload_data['contactId']
                    )
                    self._event_stream.emit('logout', payload)

                elif response.type == int(EventType.EVENT_TYPE_UNSPECIFIED):
                    pass
