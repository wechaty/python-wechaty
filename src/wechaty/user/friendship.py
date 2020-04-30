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
)
import json
import logging

from wechaty_puppet import (
    FriendshipType,
    FriendshipSearchQueryFilter,
    FriendshipPayload
)

from ..types import Acceptable
from ..accessory import Accessory

from .contact import Contact

log = logging.getLogger('FriendShip')


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
        self.friendship_id = friendship_id
        self._payload: Optional[FriendshipPayload] = None

        log.info('Friendship constructor %s', friendship_id)

        if self.__class__ is Friendship:
            raise Exception(
                'Friendship class can not be instanciated directly!')
        if self.puppet is None:
            raise Exception(
                'Friendship class can not be instanciated without a puppet!')

    @classmethod
    def load(cls, friendship_id: str) -> Friendship:
        """
        load friendship without payload, which loads in a lazy way
        :param friendship_id:
        :return: initialized friendship
        """
        return cls(friendship_id)

    @classmethod
    async def search(
            cls,
            query_filter: FriendshipSearchQueryFilter) -> Optional[Contact]:
        """
        * Search a Friend by phone or weixin.
        *
        * The best practice is to search friend request once per minute.
        * Remeber not to do this too frequently, or your account
        * may be blocked.
        """
        log.info('search() <%s, %s>', cls, query_filter)

        if query_filter.weixin is not None:
            search_response = await cls.get_puppet().friendship_search_weixin(
                weixin=query_filter.weixin
            )
        elif query_filter.phone is not None:
            search_response = await cls.get_puppet().friendship_search_phone(
                phone=query_filter.phone
            )
        else:
            raise Exception(
                'query_filter weixin/phone params should not be none'
            )
        contact = cls.get_wechaty().Contact.load(search_response.contact_id)
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
        log.info('delete() <%s>', contact.contact_id)
        # this is a dangerous action
        raise NotImplementedError

    @property
    def payload(self) -> FriendshipPayload:
        """
        get the FriendShipPayload as a property
        :return:
        """
        if self._payload is None:
            self.ready()
        if self._payload is None:
            raise Exception('can"t load friendship payload')
        return self._payload

    def __str__(self) -> str:
        """
        string format for Friendship
        """
        if self._payload is None:
            # TODO -> get constructor name of the friendship
            return 'Friendship'
        return 'Friendship # {0} <{1}>'.format(
            str(self._payload.type),
            self.payload.contact_id)

    def is_ready(self) -> bool:
        """
        check if friendship is ready
        """
        return self.puppet is None or self.payload is None

    async def ready(self):
        """
        load friendship payload
        """
        if not self.is_ready():
            friendship_search_response = await self.puppet.friendship_payload(
                id=self.friendship_id)
            self._payload = FriendshipPayload(friendship_search_response)
        if self.payload is None:
            raise Exception('can"t not load friendship payload %s'
                            % self.friendship_id)

    def contact(self) -> Contact:
        """
        get the contact of the friendship
        """
        if self.puppet is None:
            raise Exception('puppet not found ...')
        contact = self.wechaty.Contact.load(self.payload.contact_id)
        return contact

    async def accept(self):
        """
        accept friendship
        """
        log.info('accept friendship %s', self.friendship_id)
        if self.payload is None:
            raise Exception('payload not found')

        if self.payload.type != FriendshipType.FRIENDSHIP_TYPE_RECEIVE:
            # TODO -> recheck the exception string
            raise Exception(
                'accept() need type to be FriendshipType.Receive,'
                'but it got a " + Friendship.Type[this.payload.type]')
        log.info('friendship accept to %s', self.payload.contact_id)
        await self.puppet.friendship_accept(id=self.friendship_id)
        contact = self.contact()

        # reset contact data
        try:
            # TODO -> some other logical code
            # do something
            contact.ready()
        # pylint:disable=W0703
        except Exception as e:
            log.info(
                "can't reload contact data %s",
                str(e.args))
        await contact.sync()

    def hello(self) -> str:
        """
        TODO ->
        Get verify message from
        """
        if self.payload is None:
            raise Exception('payload not found')
        return self.payload.hello

    def type(self) -> FriendshipType:
        """
        Return the Friendship Type
        """
        if self.payload is None:
            return FriendshipType.FRIENDSHIP_TYPE_UNSPECIFIED
        return self.payload.type

    def to_json(self) -> str:
        """
        dumps the friendship
        """
        log.info('Friendship to_json')
        if not self.is_ready():
            raise Exception(
                f'Friendship<${self.friendship_id}> needs to be ready. '
                'Please call ready() before toJSON()')
        return json.dumps(self.payload)

    @classmethod
    async def from_json(
            cls,
            payload: Union[str, FriendshipPayload]
    ) -> Friendship:
        """
        create friendShip by friendshipJson
        """
        log.info('from_json() <%s>', payload)
        if isinstance(payload, str):
            payload = FriendshipPayload.from_json(payload)

        await cls.get_puppet().friendship_payload(
            id=payload.id, payload=json.dumps(payload)
        )
        friendship = cls.get_wechaty().Friendship.load(payload.contact_id)
        await friendship.ready()
        return friendship
