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

from collections import defaultdict
import logging

from wechaty_puppet import (
    ContactGender,
    ContactPayload,
    ContactQueryFilter,
    ContactType
)

from ..accessory import Accessory
# from wechaty import Accessory
from ..config import (
    FileBox,
)

# from wechaty.types import Sayable
# from wechaty.user.mini_program import MiniProgram
from .message import Message
from .url_link import UrlLink

if TYPE_CHECKING:
    from .tag import Tag

log = logging.getLogger('Contact')


class Contact(Accessory):
    """
    contact object
    """
    _pool: Dict[str, Contact] = defaultdict()

    def __init__(self, contact_id: str, *args, **kwargs):
        """
        initialization
        """
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
    def load(
            cls        : Type[Contact],
            contact_id : Optional[str],
            # *args,
            # **kwargs,
    ) -> Contact:
        """
        load contact by contact_id
        :param contact_id:
        :return: created contact instance
        """
        if contact_id is None:
            raise AttributeError("contact_id can't be None")
        # create new contact and set to pool
        if cls is Contact:
            raise PermissionError(
                "can't be created from abstract Contact class")

        if contact_id in cls._pool:
            return cls._pool[contact_id]

        # create new contact object
        new_contact = cls(contact_id)   # , *args, **kwargs)
        cls._pool[contact_id] = new_contact
        return new_contact

    @classmethod
    async def find(
            cls   : Type[Contact],
            query : Union[str, ContactQueryFilter],
    ):
        """
        :param query:
        :return:
        """
        raise NotImplementedError

    async def find_all(
            self,
            query: Optional[
                Union[str, ContactQueryFilter]
            ] = None
    ) -> List['Contact']:
        """
        find all contact friends
        :param query:
        :return:
        """
        log.info('Contact : <%s> find all, with queries : %s',
                 self.name,
                 str(query))

        contact_ids = await self.puppet.contact_search(query)
        contacts = [Contact.load(contact_id) for contact_id in contact_ids]

        # async load
        batch_size = 16
        # slice contacts by batch_size
        contacts = contacts[:batch_size * (len(contacts) // batch_size)]

        contact_result_list: List[Contact] = []
        for contact in contacts:
            try:
                if isinstance(contact, Contact):
                    contact.ready()
                    contact_result_list.append(contact)
            # pylint : disbale=broad-except
            except RuntimeError as e:
                name = ""
                if isinstance(contact, Contact):
                    name = contact.name
                log.info(
                    'contact<%s> exception : %s',
                    name, str(e.args))

        return contact_result_list

    def is_ready(self):
        """
        check if payload is ready
        :return:
        """
        return self.payload is not None and self.payload.name is not None

    def ready(self):
        """
        load contact object from puppet
        :return:
        """
        log.info('load contact %s', self.name)
        try:
            self.payload = self.puppet.get_contact_payload(self.contact_id)
        except Exception as e:
            log.info("can't load contact %s payload, message : %s",
                     self.name,
                     str(e.args))

            raise AttributeError("can't load contact payload")

    def __str__(self):
        """
        get contact string representation
        """
        if self.payload is None:
            return self.__init__.__name__

        if self.payload.name is not None:
            identity = self.payload.name
        elif self.payload.alias is not None:
            identity = self.payload.alias
        elif self.contact_id is not None:
            identity = self.contact_id
        else:
            identity = 'loading ...'
        return 'Contact <%s>' % identity

    async def say(self, message: Message) -> Optional[Message]:
        """
        say something
        :param message: message content
        """
        msg_id = None
        if isinstance(message, str):
            # say text
            msg_id = await self.puppet.message_send_text(
                self.contact_id, message)
        elif isinstance(message, Contact):
            msg_id = await self.puppet.message_send_contact(
                self.contact_id, message.contact_id
            )
        elif isinstance(message, FileBox):
            msg_id = await self.puppet.message_send_file(
                self.contact_id, message
            )
        elif isinstance(message, UrlLink):
            msg_id = await self.puppet.message_send_url(
                self.contact_id, message.payload
            )
        # elif isinstance(message, MiniProgram):
        #     msg_id = await self.puppet.message_send_mini_program(
        #         self.contact_id, message.payload)

        else:
            log.info("unsupported tags %s", message)
            raise RuntimeError("unsupported tags")

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

    async def alias(
            self,
            new_alias: Optional[str] = None
    ) -> Union[None, str]:
        """
        get/set alias
        """
        log.info("Contact alias <%s>", new_alias)
        if self.payload is None:
            raise Exception("Contact payload not found ...")

        if new_alias is None:
            if self.payload.alias is None:
                return ''
            return self.payload.alias

        try:
            await self.puppet.contact_alias(self.contact_id, new_alias)
            await self.puppet.contact_payload_dirty(self.contact_id)
            self.payload = await self.puppet.contact_payload(self.contact_id)

            if new_alias != self.payload.alias:
                log.info(
                    'Contact alias(%s) sync with server fail: \
                    set(%s) is not equal to get(%s)',
                    new_alias, new_alias, self.payload.alias)
        except Exception as e:
            log.info(
                'Contact alias(%s) rejected: %s',
                new_alias, str(e.args))
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
        return self.payload.type == ContactType.Offical

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
            raise Exception("contact payload not found")
        return self.payload.type

    def start(self) -> Optional[bool]:
        """
        check if it's a start account
        """
        if self.payload is None:
            return None
        return self.payload.start

    def gender(self) -> ContactGender:
        """
        get contact gender info
        """
        if self.payload is not None:
            return self.payload.gender
        return ContactGender.Unkonwn

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

    async def avatar(self) -> Optional[FileBox]:
        """
        get the avatar of the account
        """
        try:
            return await self.puppet.contact_avatar(self.contact_id)
        except Exception as e:
            log.error(
                "load contact avatar error %s",
                str(e.args))
            return None

    async def tags(self) -> List[Tag]:
        """
        Get all tags of contact
        """
        log.info("load contact tags for %s", self)
        try:
            contact_ids = await self.puppet.contact_tag_ids(self.contact_id)
            tags = [
                self.wechaty.Tag.load(contact_id)
                for contact_id
                in contact_ids]
            return tags
        except Exception as e:
            log.error(
                "load contact tags error %s",
                str(e.args))
            return []

    async def sync(self):
        """
        sync the contact data
        """
        return self.ready()

    def is_self(self) -> bool:
        """
        check if it's the self account
        """
        self_id = self.puppet.self_id()
        if self_id is None:
            return False
        return self.contact_id == self_id

    def weixin(self) -> Optional[str]:
        """
        Get the weixin number from a contact.
        """
        if self.payload is None:
            return None
        return self.payload.weixin
