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

from dataclasses import dataclass
from enum import Enum
from chatie_grpc.wechaty import (
    FriendshipType,
    FriendshipSceneType,
    FriendshipPayloadResponse
)


# pylint: disable=R0903
@dataclass
class FriendshipPayload:
    """
    friendship payload

    id: str = betterproto.string_field(1)
    contact_id: str = betterproto.string_field(2)
    hello: str = betterproto.string_field(3)
    type: "FriendshipType" = betterproto.enum_field(4)
    stranger: str = betterproto.string_field(5)
    ticket: str = betterproto.string_field(6)
    scene: "FriendshipSceneType" = betterproto.enum_field(7)

    """
    def __init__(self, response: FriendshipPayloadResponse):
        self.id = response.id
        self.contact_id = response.contact_id
        self.type = response.type
        self.hello = response.hello
        self.stranger = response.stranger
        self.ticket = response.ticket
        self.scene = response.scene

    @classmethod
    def from_json(cls, json_str: str) -> FriendshipPayload:
        """
        create friendship payload from json string
        """
        raise NotImplementedError

    id: str
    contact_id: str
    hello: str
    type: FriendshipType
    stranger: str
    ticket: str
    scene: FriendshipSceneType


# pylint: disable=R0903
@dataclass
class FriendshipSearchQueryFilter:
    """
    friendship search query filter
    """
    weixin: str
    phone: str
