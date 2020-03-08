"""
all contact component
"""

from typing import Optional, List, Type, TypeVar, Dict, Any, Union
from collections import defaultdict
from overrides import overrides
from wechaty_puppet import (
    # ContactGender,
    ContactPayload,
    ContactQueryFilter,
    # ContactType
)
from ..accessory import Accessory
# from wechaty import Accessory
from ..config import FileBox, log
# from wechaty.types import Sayable
# from wechaty.user.mini_program import MiniProgram
from .message import Message
from .tag import Tag
from .url_link import UrlLink

T = TypeVar('T', bound='Contact')


class Contact(Accessory):
    """
    contact object
    """
    _pool: Dict[str, "Contact"] = defaultdict()

    def __init__(self, contact_id: str):
        """
        initialization
        """
        self.contact_id = contact_id
        self.name = "Contact<%s>" % contact_id
        self.payload: Optional[ContactPayload] = None

    def get_id(self):
        """
        get contact_id
        :return:
        """
        return self.contact_id

    @overrides
    @classmethod
    async def say(
            cls: Type['Contact'],
            text: str,
            reply_to: Union['Contact', List['Contact']]) -> Optional[Message]:
        """
        send message interface
        :param text:
        :param reply_to:
        :return:
        """
        raise NotImplementedError

    @classmethod
    async def load(
            cls: Type[T],
            contact_id: Optional[str], *args, **kwargs) -> T:
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
        new_contact = cls(contact_id, *args, **kwargs)
        cls._pool[contact_id] = new_contact
        return new_contact

    @classmethod
    async def find(cls: Type[T], query: Optional[str or ContactQueryFilter]):
        """
        :param query:
        :return:
        """
        raise NotImplementedError

    async def find_all(
            self,
            query:
            Optional[
                Union[str, ContactQueryFilter]
            ] = None) -> List['Contact']:
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

        contact_result_list = []
        for contact in contacts:
            try:
                contact.ready()
                contact_result_list.append(contact)
            # pylint : disbale=broad-except
            except RuntimeError as e:
                log.info(
                    'contact<%s> exception : %s',
                    contact.name, str(e.args))

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

    async def sync(self) -> None:
        """
        load contact object from puppet
        :return:
        """
        await self.ready()

    async def tags(self) -> List[Tag]:
        """
        get tags
        :return: tag list
        """
        log.info('Contact tags for %s', self.name)
        try:
            tag_ids: List[str] = await self.puppet.tag_contact_list()
            tags = [self.wechaty.Tag.load(tag_id) for tag_id in tag_ids]
            return tags
        # pylint: disable=broad-except
        except Exception as e:
            log.info('load tags error %s', str(e.args))
            return []

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

    async def say(self, message: Any) -> Optional[Message]:
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
                self.contact_id, message
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
