"""
wechaty instance
"""
from typing import Optional


# pylint: disable=R0903
class WechatyOptions:
    """
    WechatyOptions instance
    """
    def __init__(self):
        """
        WechatyOptions constructor
        """
        self.io_token: str = None
        self.name: str = None
        self.profile: Optional[None or str] = None


# pylint: disable=R0903

class Wechaty:
    """
    docstring
    """
    def __init__(self):
        """
        docstring
        """
        raise NotImplementedError

    _global_instance: "Wechaty" = None

    @classmethod
    def instance(cls: "Wechaty") -> "Wechaty":
        """
        get or create global wechaty instance
        :return:
        """
        if cls._global_instance is None:
            cls._global_instance = Wechaty()
        return cls._global_instance
