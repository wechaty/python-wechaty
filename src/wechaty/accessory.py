"""
docstring
"""
from abc import ABCMeta
from typing import Optional
from wechaty_puppet.puppet import Puppet
from .config import LOG
from .wechaty import Wechaty


class Accessory:
    """
    docstring
    """
    __metaclass__ = ABCMeta
    _puppet: Optional[Puppet] = None
    # static _wechaty property to doing ...
    _wechaty: Optional[Wechaty] = None

    def __str__(self):
        """
        docstring
        :return:
        """
        raise NotImplementedError

    @classmethod
    def puppet(cls, value: Optional[Puppet] = None) -> Optional[Puppet]:
        """
        get/set global single instance of the puppet
        :return:
        """
        if value is None:
            LOG.info("get puppet instance ...")
            if cls._puppet is None:
                raise AttributeError("static puppet instance not found ...")
            return cls._puppet

        LOG.info("set puppet instance ...")
        cls._puppet = value
        return None

    @classmethod
    def wechaty(cls, value: Optional[Wechaty] = None) -> Optional[Wechaty]:
        """
        get/set wechaty instance

        If the param of value is None, then the function will return the
        instance of wechaty.Otherwise, the function will check the type
        of the value, and set as wechaty instance
        :param value:
        :return:
        """
        if value is None:
            LOG.info("get wechaty instance")
            if cls._wechaty is None:
                raise AttributeError("wechaty instance not found")
            return cls._wechaty
        if not isinstance(value, Wechaty):
            raise NameError(
                "expected wechaty instance type is Wechaty, "
                "but got %s" % value.__class__
            )
        cls._wechaty = value
        return None
