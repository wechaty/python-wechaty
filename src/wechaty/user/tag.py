"""
Tag for Contact Message
"""
from __future__ import annotations

from typing import (
    Dict,
    # Optional,
    Union,
)

from collections import defaultdict

from wechaty.accessory import Accessory
from wechaty.config import log
from wechaty.user.contact import Contact
from wechaty.user.favorite import Favorite


class Tag(Accessory):
    """
    tag object which handle the url_link content
    """
    _pool: Dict[str, Tag] = defaultdict()

    def __init__(
            self,
            tag_id: str,
    ) -> None:
        """
        initialization for tag base class
        :param tag_id:
        """
        super(Tag, self).__init__()
        log.info("create tag %s", tag_id)

        if isinstance(self, Tag):
            raise AttributeError(
                'Tag class can not be instanciated directly!'
                'See: https://github.com/Chatie/wechaty/issues/1217')

        if self.puppet is None:
            raise NotImplementedError(
                'Tag class can not be instanciated without a puppet!')

        self.tag_id: str = tag_id
        self.name: str = 'Tag <%s>' % tag_id

    @classmethod
    def load(
            cls,
            tag_id: str,
    ) -> Tag:
        """
        load tag instance
        """
        if cls is Tag:
            raise AttributeError(
                'The global Tag class can not be used directly!'
                'See: https://github.com/Chatie/wechaty/issues/1217'
            )

        if tag_id in cls._pool:
            return cls._pool[tag_id]

        new_tag = cls(tag_id)
        cls._pool[tag_id] = new_tag
        return new_tag

    @classmethod
    def get(cls, tag_id: str) -> Tag:
        """
        get tag objecr
        """
        log.info('load tag object %s', tag_id)
        return cls.load(tag_id)

    def delete(
            self,
            target: Union[Contact, Favorite] = None,
    ) -> None:
        """
        remove tag from contact or favorite
        :param target:
        :return:
        """
        log.info("delete tag %s", self.name)
        #
        if target is None:
            raise Exception("target param is required")

        if target is Contact:
            self.puppet.delete_contact_tag(self.tag_id)
        elif target is Favorite:
            self.puppet.delete_favorite_tag(self.tag_id)

    def add(
            self,
            to: Union[Contact, Favorite],
    ) -> None:
        """
        add tag to contact or favorite
        :param to:
        :return:
        """
        log.info('add tag to %s', str(to))
        if to is Contact:
            self.puppet.tag_contact_add(self.tag_id, to.get_id())
        elif to is Favorite:
            self.puppet.tag_favorite_add(self.tag_id, to.get_id())
        # to-do: tag_favorite_add

    def remove(
            self,
            source: Union[Contact, Favorite],
    ) -> None:
        """
        Remove this tag from Contact/Favorite

        tips : This function is depending on the Puppet Implementation,
        see [puppet-compatible-table](https://github.com/Chatie/
        wechaty/wiki/Puppet#3-puppet-compatible-table)
        :param source:
        :return:
        """
        log.info("remove tag for %s with %s",
                 self.tag_id,
                 str(source))
        try:
            if source is isinstance(source, Contact):
                self.puppet.tag_contact_remove(self.tag_id, source.get_id())
            # elif source is isinstance(source, Favorite):
            #     pass
        except Exception as e:
            log.info('remove exception %s', str(e.args))
            raise RuntimeError('remove error')
