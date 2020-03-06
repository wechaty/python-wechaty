"""
docstring
"""
# from abc import ABC
from typing import (
    # overload,
    Optional,
)
from wechaty_puppet import Puppet
from .config import (
    logging
)
from .wechaty import Wechaty

log = logging.getLogger('Accessory')


class AccessoryMeta(type):
    """docs"""

    _static_puppet : Optional[Puppet]  = None
    _static_wechaty: Optional[Wechaty] = None

    @property
    def puppet(cls) -> Puppet:
        """doc"""
        if cls._static_puppet is None:
            raise AttributeError('static puppet not found ...')

        return cls._static_puppet

    @puppet.setter
    def puppet(cls, new_puppet: Puppet) -> None:
        if cls._static_puppet is not None:
            raise AttributeError('static puppet can not be set twice')

        cls._static_puppet = new_puppet

    @property
    def wechaty(cls) -> Wechaty:
        """doc"""
        if cls._static_wechaty is None:
            raise AttributeError('static wechaty not found ...')
        return cls._static_wechaty

    @wechaty.setter
    def wechaty(cls, new_wechaty) -> None:
        if cls._static_wechaty is not None:
            raise AttributeError(
                'static wechaty can not be set twice'
            )
        cls._static_wechaty = new_wechaty


class Accessory(metaclass=AccessoryMeta):
    """
    docstring
    """

    _puppet : Optional[Puppet]  = None
    _wechaty: Optional[Wechaty] = None

    @property
    def puppet(self) -> Puppet:
        """doc"""
        if self._puppet is not None:
            return self._puppet

        return self.__class__.puppet

    @puppet.setter
    def puppet(self, new_puppet) -> None:
        if self._puppet is not None:
            raise AttributeError('puppet can not be set twice')

        self._puppet = new_puppet

    @property
    def wechaty(self) -> Wechaty:
        """doc"""
        if self._wechaty is not None:
            return self._wechaty
        return self.__class__.wechaty

    @wechaty.setter
    def wechaty(self, new_wechaty) -> None:
        if self._wechaty is not None:
            raise AttributeError('wechaty can not be set twice')
        self._wechaty = new_wechaty
