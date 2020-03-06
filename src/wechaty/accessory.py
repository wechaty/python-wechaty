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
    _counter: int = 0

    def __init__(self, name: str = "accessory"):
        """
        initialize the accessory instance
        """
        self.name: str = name
        # increase when Accessory is initialized
        self._counter += 1

    def __str__(self) -> str:
        """
        docstring
        :return: the base accessory class name
        """
        return "Accessory instance : %s" % self.name

    @classmethod
    def puppet(cls, value: Optional[Puppet] = None) -> Optional[Puppet]:
        """
        get/set global single instance of the puppet
        :return:
        """
        if value is None:
            if cls._puppet is None:
                raise AttributeError("static puppet instance not found ...")
            LOG.info("get puppet instance %s ...",
                     cls._puppet.name)
            return cls._puppet

        if cls._puppet is not None:
            raise AttributeError("can't set puppet instance %s twice" %
                                 cls._puppet.name)
        LOG.info("set puppet instance %s ...",
                 value.name)
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
            if cls._wechaty is None:
                raise AttributeError("wechaty instance not found")
            LOG.info("get wechaty instance %s",
                     cls._wechaty.name)
            return cls._wechaty
        if not isinstance(value, Wechaty):
            raise NameError(
                "expected wechaty instance type is Wechaty, "
                "but got %s" % value.__class__
            )
        if cls._wechaty is not None:
            raise AttributeError("can't set wechaty instance %s twice" %
                                 cls._wechaty.name)
        cls._wechaty = value
        return None
