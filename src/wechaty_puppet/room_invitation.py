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

from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from chatie_grpc.wechaty import RoomInvitationPayloadResponse

from .payload_utils import init_payload


# pylint: disable=R0903
@dataclass
class RoomInvitationPayload:
    """
    room invitation payload
    """
    def __init__(self, response: RoomInvitationPayloadResponse):
        """
        id: str = betterproto.string_field(1)
        inviter_id: str = betterproto.string_field(2)
        topic: str = betterproto.string_field(3)
        member_count: int = betterproto.uint32_field(4)
        member_ids: List[str] = betterproto.string_field(5)
        timestamp: int = betterproto.uint64_field(6)
        avatar: str = betterproto.string_field(7)
        invitation: str = betterproto.string_field(8)
        receiver_id: str = betterproto.string_field(9)
        :param response:
        """
        # init_payload(self, response)
        pass

    id: str
    invitation_id: str
    inviter_id: str
    topic: str
    member_count: int
    timestamp: int
    avatar: str
    invitation: str
    receiver_id: str
    member_ids: List[str]
    # member_id_list: List[str]
    date: datetime
