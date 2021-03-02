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
    Union,
    Optional,
    TYPE_CHECKING
)
import json

from wechaty.exceptions import WechatyOperationError
from wechaty_puppet import (  # type: ignore
    FriendshipType,
    FriendshipPayload,
    get_logger
)
# from wechaty.utils import type_check

from ..types import Acceptable
from ..accessory import Accessory

if TYPE_CHECKING:
    from .contact import Contact

log = get_logger('FriendShip')


class Friendship(Accessory, Acceptable):
    """
    Send, receive friend request, and friend confirmation events.

    * 1. send request
    * 2. receive request(in friend event)
    * 3. confirmation friendship(friend event)
    """

    Type = FriendshipType

    def __init__(self, friendship_id: str):
        """
        initialization constructor for friendship
        """
        super(Friendship, self).__init__()

        self.friendship_id = friendship_id

        log.info('Friendship constructor %s', friendship_id)

    @classmethod
    def load(cls, friendship_id: str) -> Friendship:
        """
        load friendship without payload, which loads in a lazy way
        :param friendship_id:
        :return: initialized friendship
        """
        return cls(friendship_id)

    @classmethod
    async def search(cls, weixin: Optional[str] = None,
                     phone: Optional[str] = None) -> Optional[Contact]:
        """
        * Search a Friend by phone or weixin.
        *
        * The best practice is to search friend request once per minute.
        * Remeber not to do this too frequently, or your account
        * may be blocked.
        """
        log.info('search() <%s, %s, %s>', cls, weixin, phone)
        friend_id = await cls.get_puppet().friendship_search(weixin=weixin,
                                                             phone=phone)
        if friend_id is None:
            return None
        contact = cls.get_wechaty().Contact.load(friend_id)
        await contact.ready()
        return contact

    @classmethod
    async def add(cls, contact: Contact, hello: str):
        """
        add friendship
        """
        log.info('add() <%s, %s>', contact.contact_id, hello)
        await cls.get_puppet().friendship_add(
            contact_id=contact.contact_id, hello=hello
        )

    @classmethod
    async def delete(cls, contact: Contact):
        """
        delete friendship
        """
        log.info('delete() a contact <%s>', contact.contact_id)
        log.warning('trying to delete a friend, which is dangerous, is not '
                    'implemented')
        # this is a dangerous action
        raise NotImplementedError

    def __str__(self) -> str:
        """
        string format for Friendship
        """
        if self._payload is None:
            return 'Friendship <{0}>'.format(self.friendship_id)
        return 'Friendship # type: {0}  contact: <{1}>  hello msg: <{2}>' \
            .format(self.type().name, self._payload.contact_id, self.hello())

    async def ready(self, force_sync: bool = False):
        """
        load friendship payload
        """
        log.info('ready() sync the friendship payload')
        if not self.is_ready() or force_sync:
            self._payload = await self.puppet.friendship_payload(
                friendship_id=self.friendship_id)

    def contact(self) -> Contact:
        """
        get the contact of the friendship
        """

        contact = self.wechaty.Contact.load(self.payload.contact_id)
        return contact

    async def accept(self):
        """
        accept friendship
        """
        log.info('accept friendship, friendship_id: <%s>', self.friendship_id)
        if self.type() != FriendshipType.FRIENDSHIP_TYPE_RECEIVE:
            raise WechatyOperationError(
                'accept() need type to be FriendshipType.'
                'FRIENDSHIP_TYPE_RECEIVE, but it got a " + FriendshipType : '
                '<{0}>'.format(self.type().name))

        log.info('friendship accept to %s', self.payload.contact_id)
        await self.puppet.friendship_accept(friendship_id=self.friendship_id)
        contact = self.contact()

        # reset contact data
        try:
            # TODO -> some other logical code
            await contact.ready()
        # pylint:disable=W0703
        except Exception as e:
            log.info(
                "can't reload contact data %s",
                str(e.args))

    def hello(self) -> str:
        """
        TODO ->
        Get verify message from
        """
        if self.payload.hello is None:
            hello_msg = ''
        else:
            hello_msg = self.payload.hello

        log.info('get hello message <%s> of friendship <%s>', hello_msg, self.payload)

        return hello_msg

    def type(self) -> FriendshipType:
        """
        Return the Friendship Type
        """
        if self.payload is None:
            return FriendshipType.FRIENDSHIP_TYPE_UNSPECIFIED
        if isinstance(self.payload.type, int):
            return FriendshipType(self.payload.type)
        elif isinstance(self.payload.type, FriendshipType):
            return self.payload.type
        else:
            raise TypeError('friendship type field type is limited between '
                            'int/FriendshipType')

    def to_json(self) -> str:
        """
        dumps the friendship
        """
        log.info('Friendship to_json')
        return json.dumps(self.payload)

    @classmethod
    async def from_json(
        cls,
        json_data: Union[str, FriendshipPayload]
    ) -> Friendship:
        """
        create friendShip by friendshipJson
        """
        log.info('from_json() <%s>', json_data)
        if isinstance(json_data, str):
            payload = FriendshipPayload(**json.loads(json_data))
        else:
            payload = json_data

        await cls.get_puppet().friendship_payload(
            friendship_id=payload.id, payload=payload
        )
        friendship = cls.get_wechaty().Friendship.load(payload.contact_id)
        await friendship.ready()
        return friendship
