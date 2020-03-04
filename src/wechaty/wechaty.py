"""
wechaty instance
"""
from typing import Optional
from .config import LOG


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

    _global_instance: Optional["Wechaty"] = None

    async def start(self) -> None:
        """
        start the wechaty
        :return:
        """
        LOG.info("wechaty is starting ...")

    async def stop(self) -> None:
        """
        stop the wechaty
        """
        LOG.info("wechaty is stoping ...")
