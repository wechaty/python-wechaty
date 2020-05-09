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
from typing import Optional, List

from dataclasses import dataclass


@dataclass
class RoomMemberQueryFilter:
    """
    room member query filter
    """
    name: Optional[str] = None
    room_alias: Optional[str] = None
    contact_alias: Optional[str] = None


@dataclass
class RoomQueryFilter:
    """
    query filter for room
    """
    id: Optional[str] = None
    topic: Optional[str] = None


@dataclass
class RoomPayload:
    """
    room payload data structure
    """
    id: str
    topic: str
    admin_ids: Optional[List[str]] = None
    avatar: Optional[str] = None
    member_ids: Optional[List[str]] = None
    owner_id: Optional[str] = None


@dataclass
class RoomMemberPayload:
    """
    room member payload structure
    """
    id: str
    avatar: str
    name: str

    room_alias: Optional[str] = None
    inviter_id: Optional[str] = None
