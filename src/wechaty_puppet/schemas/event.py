"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2018-now @copyright Wechaty

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
from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class ScanStatus(Enum):
    """
    scan status enum
    """
    Unknown = 0
    Cancel = 1
    Waiting = 2
    Scanned = 3
    Confirmed = 4
    Timeout = 5


@dataclass
class EventPayloadBase:
    pass


@dataclass
class EventFriendshipPayload(EventPayloadBase):
    friendship_id: str


@dataclass
class EventLoginPayload(EventPayloadBase):
    contact_id: str


@dataclass
class EventLogoutPayload(EventPayloadBase):
    contact_id: str
    data: str


@dataclass
class EventMessagePayload(EventPayloadBase):
    message_id: str
    type: Optional[str] = None
    from_id: Optional[str] = None
    filename: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[float] = None
    room_id: Optional[str] = None
    to_id: Optional[str] = None
    mention_ids: Optional[List[str]] = None


@dataclass
class EventRoomInvitePayload(EventPayloadBase):
    room_invitation_id: str


@dataclass
class EventRoomJoinPayload(EventPayloadBase):
    # TODO -> discuss name style
    invited_ids: List[str]
    inviter_id: str
    room_id: str
    time_stamp: float

@dataclass
class EventRoomLeavePayload(EventPayloadBase):
    # TODO -> discuss name style
    removed_ids: List[str]
    remover_id: str
    room_id: str
    time_stamp: float


@dataclass
class EventRoomTopicPayload(EventPayloadBase):
    changer_id: str
    new_topic: str
    old_topic: str
    room_id: str
    time_stamp: float


@dataclass
class EventScanPayload(EventPayloadBase):
    status: ScanStatus
    qrcode: Optional[str] = None
    data: Optional[str] = None


@dataclass
class EventDongPayload(EventPayloadBase):
    data: Optional[str] = None


@dataclass
class EventErrorPayload(EventPayloadBase):
    data: str


@dataclass
class EventReadyPayload(EventPayloadBase):
    data: str


@dataclass
class EventResetPayload(EventPayloadBase):
    data: str


@dataclass
class EventHeartbeatPayload(EventPayloadBase):
    data: str
