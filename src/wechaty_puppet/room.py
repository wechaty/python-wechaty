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
from .payload_utils import init_payload

from chatie_grpc.wechaty import (
    RoomPayloadResponse,
    RoomMemberPayloadResponse
)


# pylint: disable=R0903
class RoomQueryFilter:
    """
    query filter for room
    """
    def __init__(self, query: str = None):
        """
        initialization
        """
        self.query: Optional[str] = query


class RoomMemberQueryFilter:
    """
    query filter for room member
    """
    def __init__(self):
        """
        initialization for RoomMemberQueryFilter
        """
        raise NotImplementedError


@dataclass
class RoomPayload:
    """
    room payload
    """
    def __init__(self, response: RoomPayloadResponse):
        """
        initialization for room payload

        id: str = betterproto.string_field(1)
        topic: str = betterproto.string_field(2)
        avatar: str = betterproto.string_field(3)
        owner_id: str = betterproto.string_field(4)
        admin_ids: List[str] = betterproto.string_field(5)
        member_ids: List[str] = betterproto.string_field(6)
        """
        init_payload(self, response)

    id: str
    topic: str
    owner_id: str
    avatar: str
    admin_ids: List[str]
    member_ids: List[str]


@dataclass
class RoomMemberPayload:
    """
    room member payload
    """
    def __init__(self, response: RoomMemberPayloadResponse):
        init_payload(self, response)

    id: str
    room_alias: str
    inviter_id: str
    avatar: str
    name: str

