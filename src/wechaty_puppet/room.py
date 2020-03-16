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


# pylint: disable=R0903
class RoomQueryFilter:
    """
    query filter for room
    """
    def __init__(self):
        """
        initialization
        """
        raise NotImplementedError


class RoomMemberQueryFilter:
    """
    query filter for room member
    """
    def __init__(self):
        """
        initialization for RoomMemberQueryFilter
        """
        raise NotImplementedError


class RoomPayload:
    """
    room payload
    """
    def __init__(self):
        """
        initialization for room payload
        """
        raise NotImplementedError
