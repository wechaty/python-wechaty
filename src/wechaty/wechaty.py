"""
wechaty instance
"""
#
# Python 3.7: PEP 563: Postponed Evaluation of Annotations
#   https://docs.python.org/3.7/whatsnew/3.7.html#pep-563-postponed-evaluation-of-annotations
from __future__ import annotations

from typing import (
    cast,
    ClassVar,
    Optional,
    # Type,
    # Union,
)

from .config import (
    logging,
)

log = logging.getLogger('Wechaty')


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


class Wechaty:
    """
    docstring
    """

    _global_instance: ClassVar[Optional[Wechaty]] = None

    def __init__(self):
        """
        docstring
        """
        log.info('__init__()')
        raise NotImplementedError

    @classmethod
    def instance(cls: Wechaty) -> Wechaty:
        """
        get or create global wechaty instance
        :return:
        """
        log.info('instance()')

        if cls._global_instance is None:
            cls._global_instance = Wechaty()

        return cast(Wechaty, cls._global_instance)

    async def start(self) -> None:
        """
        start the wechaty
        :return:
        """
        log.info("wechaty is starting ...")

    async def stop(self) -> None:
        """
        stop the wechaty
        """
        log.info("wechaty is stoping ...")
