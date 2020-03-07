"""
docstring
"""
# pylint:disable=protected-access

from typing import (
    # overload,
    # cast,
    Optional,
)
from wechaty_puppet import Puppet
from .config import (
    logging
)
from .wechaty import Wechaty

log = logging.getLogger('Accessory')


#
# Huan(202003):
#   Create this AccessoryMeta class to
#   implemente a property access behavior
#   for the Accessory class
#   by setting it as the `metaclass` of `Accessory`
#
class AccessoryMeta(type):
    """docs"""

    # https://stackoverflow.com/a/42029208/1123955
    def __setattr__(cls, name, value):
        # print('__setattr__', cls, name, value)
        # print('super()', super())
        if not hasattr(cls, name):     # would this create a new attribute?
            raise AttributeError('Creating new attributes is not allowed!')

        # https://stackoverflow.com/a/15751135/1123955
        propobj = getattr(cls, name, None)

        # print(propobj)
        if isinstance(propobj, property):
            # print("setting attr %s using property's fset'" % name)
            if propobj.fset is None:
                raise AttributeError("can't set attribute")
            propobj.fset(cls, value)
        else:
            # print('setting attr %s to %s' % (name, value))
            super().__setattr__(name, value)


#
# Huan(202003)
#   The Python Class have different behavior compare to ES6 & Java/C++:
#       If you have a static (@classmethod) in your class,
#       and you have a instance method in your class,
#       and they are same name...
#       Then, the instance value will overwrite the static value.
#       The same as the properties.
#
class Accessory(metaclass=AccessoryMeta):
    """
    docstring
    """

    _puppet : Optional[Puppet]  = None
    _wechaty: Optional[Wechaty] = None

    @property
    def puppet(self) -> Puppet:
        """doc"""
        if self._puppet is None:
            raise AttributeError('_puppet not set')
        return self._puppet

    @puppet.setter
    def puppet(self, new_puppet: Puppet) -> None:
        if self._puppet is not None:
            raise AttributeError('_puppet can not be set twice')

        self._puppet = new_puppet

    @property
    def wechaty(self) -> Wechaty:
        """doc"""
        if self._wechaty is None:
            raise AttributeError('_wechaty not set')
        return self._wechaty

    @wechaty.setter
    def wechaty(self, new_wechaty: Wechaty) -> None:
        if self._wechaty is not None:
            raise AttributeError('_wechaty can not be set twice')
        self._wechaty = new_wechaty
