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
from enum import Enum
from typing import List
from typing import Optional

from dataclasses import dataclass


class MessageType(Enum):
    """
    doc
    """
    Unknown = 0
    Attachment = 1
    Audio = 2
    Contact = 3
    ChatHistory = 4
    Emoticon = 5
    Image = 5
    Text = 6
    Location = 7
    MiniProgram = 8

    Transfer = 9
    RedEnvelope = 10

    Recalled = 11
    Url = 12
    Video = 13


class WechatAppMessageType(Enum):
    Text = 1
    Img = 2
    Audio = 3
    Video = 4
    Url = 5
    Attach = 6
    Open = 7
    Emoji = 8
    VoiceRemind = 9
    ScanGood = 10
    Good = 13
    Emotion = 15
    CardTicket = 16
    RealtimeShareLocation = 17
    ChatHistory = 19
    MiniProgram = 33
    Transfers = 2000
    RedEnvelopes = 2001
    ReaderType = 100001


class WechatMessageType(Enum):
    Text = 1
    Image = 3
    Voice = 34
    VerifyMsg = 37
    PossibleFriendMsg = 40
    ShareCard = 42
    Video = 43
    Emoticon = 47
    Location = 48
    App = 49
    VoipMsg = 50
    StatusNotify = 51
    VoipNotify = 52
    VoipInvite = 53
    MicroVideo = 62
    # 转账
    Transfer = 2000
    # 红包
    RedEnvelope = 2001
    # 小程序
    MiniProgram = 2002
    # 群邀请
    GroupInvite = 2003
    # 文件消息
    File = 2004
    SysNotice = 9999
    Sys = 10000
    # NOTIFY 服务通知
    Recalled = 10002


@dataclass
class MessagePayloadBase:
    id: str
    mention_ids: List[str]

    time_stamp: float
    type: MessageType

    file_name: Optional[str] = None
    text: Optional[str] = None


@dataclass
class MessagePayloadRoom:

    room_id: str
    from_id: Optional[str] = None

    # if to is not set, then room must be set
    to_id: Optional[str] = None


@dataclass
class MessagePayloadTo:
    from_id: str

    # if to is not set, then room must be set
    to_id: str

    room_id: Optional[str] = None


@dataclass
class EventMessagePayload:
    message_id: str


@dataclass
class MessagePayload:
    id: str
    mention_ids: List[str]

    time_stamp: float
    type: MessageType
    from_id: str

    file_name: Optional[str] = None
    text: Optional[str] = None

    to_id: Optional[str] = None
    room_id: Optional[str] = None


@dataclass
class MessageQueryFilter:
    from_id: Optional[str] = None
    id: Optional[str] = None
    room_id: Optional[str] = None
    text: Optional[str] = None
    to_id: Optional[str] = None
    type: Optional[MessageType] = None
