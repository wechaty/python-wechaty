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

import types
import asyncio
import dataclasses
import json
from asyncio import Task
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Type,
    Union,
    Callable,
)

from pyee import AsyncIOEventEmitter  # type: ignore

from wechaty.exceptions import WechatyPayloadError, WechatyOperationError
from wechaty.config import PARALLEL_TASK_NUM
from wechaty.utils.async_helper import gather_with_concurrency
from wechaty_puppet import (
    ContactGender,
    ContactPayload,
    ContactQueryFilter,
    ContactType,

    get_logger,
    FileBox
)
# from wechaty.utils import type_check

from ..accessory import Accessory

if TYPE_CHECKING:
    # pytype: disable=pyi-error
    from .tag import Tag
    # pytype: disable=pyi-error
    from .message import Message
    # pytype: disable=pyi-error
    from .url_link import UrlLink

log = get_logger('Contact')


# pylint:disable=R0904
class Contact(Accessory[ContactPayload], AsyncIOEventEmitter):
    """
    contact object
    """
    _pool: Dict[str, 'Contact'] = {}

    def __init__(self, contact_id: str):
        """
        initialization
        """
        super().__init__()
        self.contact_id: str = contact_id
        self.payload: Optional[ContactPayload] = None

    def get_id(self) -> str:
        """
        get contact_id
        :return:
        """
        return self.contact_id

    @classmethod
    def load(cls: Type[Contact], contact_id: str) -> Contact:
        """
        load contact by contact_id
        :param contact_id:
        :return: created contact instance
        """
        # create new contact and set to pool

        if contact_id in cls._pool:
            return cls._pool[contact_id]

        # create new contact object
        new_contact = cls(contact_id)  # , *args, **kwargs)
        cls._pool[contact_id] = new_contact
        return new_contact

    @classmethod
    def _filter_contacts(cls,
                         contacts: List[Contact],
                         query: Union[str, ContactQueryFilter, Callable[[Contact], bool]]) -> List[Contact]:

        func: Callable[[Contact], bool]
        if isinstance(query, str):

            def filter_func(contact: Contact) -> bool:
                payload = contact.payload
                if not payload:
                    return False
                if query in payload.alias or query in payload.name:
                    return True
                if query == payload.id or quit == payload.weixin:
                    return True
                return False
            func = filter_func

        elif isinstance(query, ContactQueryFilter):

            def filter_func(contact: Contact) -> bool:
                payload = contact.payload

                # to pass the type checking
                assert isinstance(query, ContactQueryFilter)
                if not payload:
                    return False

                if query.alias and query.alias in payload.alias:
                    return True
                if query.name and query.name in payload.name:
                    return True

                if query.id and query.id == payload.id:
                    return True
                if query.weixin and query.weixin == payload.weixin:
                    return True

                return False
            func = filter_func
        elif isinstance(types, types.FunctionType):
            func = query
        else:
            raise WechatyOperationError(f'Query Argument<{query}> is not correct')

        assert not not func
        contacts = list(filter(func, contacts))
        return contacts

    @classmethod
    async def find(cls,
                   query: Union[str, ContactQueryFilter, Callable[[Contact], bool]]
                   ) -> Optional[Contact]:
        """
        find the first of contacts based on query, which can be string, ContactQueryFilter, or callable<filter> function

        Args:
            query: the query body to build filter
        Args:
            query:

        Examples:
            >>> # 1. find contacts based query string, will match one of: contact_id, weixin, name and alias
            >>> # what's more, contact_id and weixin will follow extract match, name and alias will follow fuzzy match
            >>> Contact.find('your-contact-id/weixin')   # find: <your-contact-id> == contact.contact_id
            >>> Contact.find('name/alias')     # find: <name> in contact.name

            >>> # 2. find contacts based ContactQueryFilter object, will match all fields
            >>> query = ContactQueryFilter(id='your-contact-id', weixin='weixin')     # find: <your-contact-id> == contact.contact_id
            >>> query = ContactQueryFilter(name='your-contact-name')      # find: <your-contact-name> in contact.name
            >>> Contact.find(query)

            >>> # 3. find contacts based on callable query function
            >>> def filter_contacts(contact: Contact) -> bool:
            >>>     if contact.contact_id == "your-contact-id":
            >>>         return True
            >>>     return False
            >>> Contact.find(filter_contacts)
        Returns: filtered contact, None or Contact
        """
        log.info('find() <%s, %s>', cls, query)

        contacts = await cls.find_all(query)
        if not contacts:
            return None
        return contacts[0]

    @classmethod
    async def find_all(cls: Type[Contact],
                       query: Optional[Union[str, ContactQueryFilter, Callable[[Contact], bool]]] = None
                       ) -> List[Contact]:
        """
        find all contacts based on query, which can be string, ContactQueryFilter, or callable<filter> function

        Args:
            query: the query body to build filter
        Args:
            query:

        Examples:
            >>> # 1. find contacts based query string, will match one of: contact_id, weixin, name and alias
            >>> # what's more, contact_id and weixin will follow extract match, name and alias will follow fuzzy match
            >>> Contact.find_all('your-contact-id/weixin')   # find: <your-contact-id> == contact.contact_id
            >>> Contact.find_all('name/alias')     # find: <name> in contact.name

            >>> # 2. find contacts based ContactQueryFilter object, will match all fields
            >>> query = ContactQueryFilter(id='your-contact-id', weixin='weixin')     # find: <your-contact-id> == contact.contact_id
            >>> query = ContactQueryFilter(name='your-contact-name')      # find: <your-contact-name> in contact.name
            >>> Contact.find_all(query)

            >>> # 3. find contacts based on callable query function
            >>> def filter_contacts(contact: Contact) -> bool:
            >>>     if contact.contact_id == "your-contact-id":
            >>>         return True
            >>>     return False
            >>> Contact.find_all(filter_contacts)
        Returns: filtered contacts/
        """
        log.info('find_all() <%s, %s>', cls, query)

        # 1. load contacts with concurrent tasks
        contact_ids: List[str] = await cls.get_puppet().contact_list()

        contacts: List[Contact] = [cls.load(contact_id) for contact_id in contact_ids]
        tasks: List[Task] = [asyncio.create_task(contact.ready()) for contact in contacts]
        await gather_with_concurrency(PARALLEL_TASK_NUM, tasks)

        # 2. filter contacts
        if not query:
            return contacts


        return contacts

    async def ready(self, force_sync: bool = False) -> None:
        """
        load contact object from puppet
        :return:
        """

        if force_sync or not self.is_ready():
            try:
                self.payload = await self.puppet.contact_payload(
                    self.contact_id)
                log.info('load contact <%s>', self)
            except IOError as e:
                log.info('can"t load contact %s payload, message : %s',
                         self.name,
                         str(e.args))

                raise WechatyPayloadError('can"t load contact payload')

    def __str__(self) -> str:
        """
        get contact string representation
        """
        if not self.is_ready() or not self.payload:
            return 'Contact <{}>'.format(self.contact_id)

        if self.payload.alias.strip() != '':
            identity = self.payload.alias
        elif self.payload.name.strip() != '':
            identity = self.payload.name
        elif self.contact_id.strip() != '':
            identity = self.contact_id
        else:
            identity = 'loading ...'
        return 'Contact <%s> <%s>' % (self.contact_id, identity)

    async def say(self, message: Union[str, Message, FileBox, Contact, UrlLink]
                  ) -> Optional[Message]:
        """
        say something
        :param message: message content
        """
        if not message:
            log.error('can"t say nothing')
            return None

        if not self.is_ready():
            await self.ready()

        # import some class because circular dependency
        from wechaty.user.url_link import UrlLink

        if isinstance(message, str):
            # say text
            msg_id = await self.puppet.message_send_text(
                conversation_id=self.contact_id,
                message=message
            )
        elif isinstance(message, Contact):
            msg_id = await self.puppet.message_send_contact(
                contact_id=message.contact_id,
                conversation_id=self.contact_id
            )

        elif isinstance(message, FileBox):
            msg_id = await self.puppet.message_send_file(
                conversation_id=self.contact_id,
                file=message
            )

        elif isinstance(message, UrlLink):
            # use this way to resolve circulation dependency import
            msg_id = await self.puppet.message_send_url(
                conversation_id=self.contact_id,
                url=json.dumps(dataclasses.asdict(message.payload))
            )
        # elif isinstance(message, MiniProgram):
        #     msg_id = await self.puppet.message_send_mini_program(
        #         self.contact_id, message.payload)

        else:
            log.info('unsupported tags %s', message)
            raise WechatyOperationError('unsupported tags')

        if msg_id is not None:
            msg = self.wechaty.Message.load(msg_id)
            await msg.ready()
            return msg

        return None

    @property
    def name(self) -> str:
        """
        get contact name
        """
        if not self.payload:
            return ''
        return self.payload.name

    async def alias(self,
                    new_alias: Optional[str] = None
                    ) -> Union[None, str]:
        """
        get/set alias
        """
        log.info('Contact alias <%s>', new_alias)
        if not self.is_ready():
            await self.ready()

        if self.payload is None:
            raise WechatyPayloadError('can"t load contact payload <%s>' % self)

        try:
            alias = await self.puppet.contact_alias(self.contact_id, new_alias)

            # reload the contact payload
            await self.ready(force_sync=True)
            return alias
        # pylint:disable=W0703
        except Exception as exception:
            log.info(
                'Contact alias(%s) rejected: %s',
                new_alias, str(exception.args))
        return None

    def is_friend(self) -> Optional[bool]:
        """
        Check if contact is friend

        False for not friend of the bot, null for unknown.
        """
        if not self.payload or not self.payload.friend:
            return None
        return self.payload.friends

    def is_offical(self) -> bool:
        """
        Check if it's a offical account
        :params:
        :return:
        """
        if self.payload is None:
            return False
        return self.payload.type == ContactType.CONTACT_TYPE_OFFICIAL

    def is_personal(self) -> bool:
        """
        Check if it's a personal account
        """
        if self.payload is None:
            return False
        return self.payload.type == ContactType.CONTACT_TYPE_PERSONAL

    def type(self) -> ContactType:
        """
        get contact type
        """
        if self.payload is None:
            raise WechatyPayloadError('contact payload not found')
        return self.payload.type

    def star(self) -> Optional[bool]:
        """
        check if it's a star account
        """
        if self.payload is None:
            return None
        return self.payload.star

    def gender(self) -> ContactGender:
        """
        get contact gender info
        """
        if self.payload is not None:
            return self.payload.gender
        return ContactGender.CONTACT_GENDER_UNSPECIFIED

    def province(self) -> Optional[str]:
        """
        get the province of the account
        """
        if self.payload is None:
            return None
        return self.payload.province

    def city(self) -> Optional[str]:
        """
        get the city of the account
        """
        if self.payload is None:
            return None
        return self.payload.city

    async def avatar(self, file_box: Optional[FileBox] = None) -> FileBox:
        """
        get the avatar of the account
        """
        avatar = await self.puppet.contact_avatar(
            contact_id=self.contact_id, file_box=file_box)
        return avatar

    async def tags(self) -> List[Tag]:
        """
        Get all tags of contact
        """
        log.info('load contact tags for %s', self)
        tag_ids = await self.puppet.tag_contact_list(self.contact_id)
        tags = [self.wechaty.Tag.load(tag_id)
                for tag_id in tag_ids]
        return tags

    async def sync(self) -> None:
        """
        sync the contact data
        """
        await self.ready()

    def is_self(self) -> bool:
        """
        check if it's the self account
        """
        return self.wechaty.contact_id == self.contact_id

    def weixin(self) -> Optional[str]:
        """
        Get the weixin number from a contact.
        """
        if self.payload is None:
            return None
        return self.payload.weixin
