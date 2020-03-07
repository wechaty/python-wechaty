"""
Python Wechaty - https://github.com/wechaty/python-wechaty

2020-now @copyright Wechaty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
#
# Python 3.7: PEP 563: Postponed Evaluation of Annotations
#   https://docs.python.org/3.7/whatsnew/3.7.html#pep-563-postponed-evaluation-of-annotations
from __future__ import annotations

from typing import (
    cast,
    ClassVar,
    Optional,
    Type,
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
    def instance(cls: Type[Wechaty]) -> Wechaty:
        """
        get or create global wechaty instance
        :return:
        """
        log.info('instance()')

        if cls._global_instance is None:
            cls._global_instance = cls()

        # Huan(202003): how to remove cast?
        return cast(Wechaty, cls._global_instance)
        # return cls._global_instance

    async def start(self) -> None:
        """
        start the wechaty
        :return:
        """
        log.info('wechaty is starting ...')

    async def stop(self) -> None:
        """
        stop the wechaty
        """
        log.info('wechaty is stoping ...')
