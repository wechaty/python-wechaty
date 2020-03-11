"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    List,
)

if TYPE_CHECKING:
    from .tag import Tag


# pylint: disable=R
class Favorite:
    """
    favorite object which handle the url_link content
    """
    def __init__(self, favorite_id: str):
        self.favorite_id = favorite_id
        raise NotImplementedError

    def get_id(self):
        """
        get favorite_id
        :return:
        """
        return self.favorite_id

    async def tags(self) -> List[Tag]:
        """
        get favorite tags
        """
        # TODO
        return []

    async def find_all(self) -> List[Tag]:
        """
        get all favorite tags
        """
        # TODO
        return []
