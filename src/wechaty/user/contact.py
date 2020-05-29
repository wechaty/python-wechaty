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
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Type,
    Union,
)

from pyee import AsyncIOEventEmitter    # type: ignore
from wechaty_puppet import (    # type: ignore
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
class Contact(Accessory, AsyncIOEventEmitter):
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
        # name = "Contact<" + contact_id  + ">"
        # self.name: str = "default_acontact"
        self.payload: Optional[ContactPayload] = None

    def get_id(self):
        """
        get contact_id
        :return:
        """
        return self.contact_id

    @classmethod
    def load(cls: Type[Contact], contact_id: Optional[str]) -> Contact:
        """
        load contact by contact_id
        :param contact_id:
        :return: created contact instance
        """
        if contact_id is None:
            raise AttributeError('contact_id can"t be None')
        # create new contact and set to pool

        # if cls is Contact:
        #     raise PermissionError(
        #         'can"t be created from abstract Contact class')

        if contact_id in cls._pool:
            return cls._pool[contact_id]

        # create new contact object
        new_contact = cls(contact_id)  # , *args, **kwargs)
        cls._pool[contact_id] = new_contact
        return new_contact

    @classmethod
    async def find(cls: Type[Contact], query: Union[str, ContactQueryFilter]) \
            -> Optional[Contact]:
        """
        find a single target contact
        :param query:
        :return:
        """
        log.info('find() <%s, %s>', cls, query)
        contact_list = await cls.find_all(query)
        if len(contact_list) == 0:
            return None
        return contact_list[0]

    @classmethod
    async def find_all(cls: Type[Contact],
                       query: Optional[Union[str, ContactQueryFilter]] = None
                       ) -> List[Contact]:
        """
        find all contact friends
        :param query:
        :return:
        """
        log.info('find_all() <%s, %s>', cls, query)

        contact_ids = await cls.get_puppet().contact_list()
        contacts = [Contact.load(contact_id) for contact_id in contact_ids]

        # async load
        batch_size = 16
        # slice contacts by batch_size
        contacts = contacts[:batch_size * (len(contacts) // batch_size)]

        contact_result_list: List[Contact] = []

        for contact in contacts:
            try:
                await contact.ready()
                contact_result_list.append(contact)
            except RuntimeError as exception:
                log.info('load contact occur exception: %s', exception.args)

        return contact_result_list

    def is_ready(self):
        """
        check if payload is ready
        :return:
        """
        return self.payload is not None and self.payload.name is not None

    async def ready(self, force_sync: bool = False):
        """
        load contact object from puppet
        :return:
        """

        if force_sync or not self.is_ready():
            try:
                payload = await self.puppet.contact_payload(
                    self.contact_id)

                self.payload = payload
                log.info('load contact <%s>', self)
            except IOError as e:
                log.info('can"t load contact %s payload, message : %s',
                         self.name,
                         str(e.args))

                raise IOError('can"t load contact payload')

    def __str__(self):
        """
        get contact string representation
        """
        if self.payload is None:
            return 'Contact <{}>'.format(self.contact_id)

        if self.payload.alias.strip() != '':
            identity = self.payload.alias
        elif self.payload.name.strip() != '':
            identity = self.payload.name
        elif self.contact_id.strip() != '':
            identity = self.contact_id
        else:
            identity = 'loading ...'
        return 'Contact <%s>' % identity

    async def say(self, message: Union[str, Message, FileBox, Contact, UrlLink]
                  ) -> Optional[Message]:
        """
        say something
        :param message: message content
        """
        if not self.is_ready():
            await self.ready()

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
                url=message.url
            )
        # elif isinstance(message, MiniProgram):
        #     msg_id = await self.puppet.message_send_mini_program(
        #         self.contact_id, message.payload)

        else:
            log.info('unsupported tags %s', message)
            raise RuntimeError('unsupported tags')

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
        if self.payload is not None and self.payload.name is not None:
            return self.payload.name
        return ''

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
            raise Exception('can"t load contact payload <%s>' % self)

        if new_alias is None:
            await self.ready()
            if self.payload.alias is None:
                return ''
            return self.payload.alias

        try:
            await self.puppet.contact_alias(self.contact_id, new_alias)
            await self.ready(force_sync=True)
            if new_alias != self.payload.alias:
                log.info(
                    'Contact alias(%s) sync with server fail: \
                    set(%s) is not equal to get(%s)',
                    new_alias, new_alias, self.payload.alias)
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
        if self.payload is None or self.payload is None:
            return None
        return self.payload.friend

    def is_offical(self) -> bool:
        """
        Check if it's a offical account
        :params:
        :return:
        """
        if self.payload is None:
            return False
        return self.payload.type == ContactType.Official

    def is_personal(self) -> bool:
        """
        Check if it's a personal account
        """
        if self.payload is None:
            return False
        return self.payload.type == ContactType.Personal

    def type(self) -> ContactType:
        """
        get contact type
        """
        if self.payload is None:
            raise Exception('contact payload not found')
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
        return ContactGender.Unknown

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

    async def avatar(self, file_box: Optional[FileBox]) -> FileBox:
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

    async def sync(self):
        """
        sync the contact data
        """
        return self.ready()

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
