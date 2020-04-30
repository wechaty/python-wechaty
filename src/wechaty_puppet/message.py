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
from typing import List, Type
from typing import Optional
from datetime import datetime

from dataclasses import dataclass

from chatie_grpc.wechaty import (
    MessagePayloadResponse,
    MessageType
)


# use MessageType of chatie_grpc instead

# class MessageType(Enum):
#     """
#     doc
#     * - MessageType.Unknown     </br>
#     * - MessageType.Attachment  </br>
#     * - MessageType.Audio       </br>
#     * - MessageType.Contact     </br>
#     * - MessageType.Emoticon    </br>
#     * - MessageType.Image       </br>
#     * - MessageType.Text        </br>
#     * - MessageType.Video       </br>
#     * - MessageType.Url         </br>
#     """
#     Unknown = 0
#     Attachment = 1
#     Audio = 2
#     Contact = 3
#     Emoticon = 4
#     Image = 5
#     Text = 6
#     Video = 7
#     Url = 8
#     Recalled = 9
#     MiniProgram = 10


# pylint: disable=R0903
@dataclass()
class MessagePayload:
    """
    doc
    """
    id: str
    filename: str
    text: str
    timestamp: float
    type: MessageType
    from_id: str
    room_id: str
    to_id: str
    mention_ids: List[str]

    @classmethod
    def from_puppet_response(cls, response: MessagePayloadResponse):
        """
        create message payload from puppet response
        :param response:
            id: str = betterproto.string_field(1)
            filename: str = betterproto.string_field(2)
            text: str = betterproto.string_field(3)
            timestamp: int = betterproto.uint64_field(4)
            type: "MessageType" = betterproto.enum_field(5)
            from_id: str = betterproto.string_field(6)
            room_id: str = betterproto.string_field(7)
            to_id: str = betterproto.string_field(8)
            mention_ids: List[str] = betterproto.string_field(9)
        :return:
        """
        return cls(
            id=response.id,
            filename=response.filename,
            text=response.text,
            timestamp=response.timestamp,
            type=response.type,
            from_id=response.from_id,
            room_id=response.room_id,
            to_id=response.to_id,
            mention_ids=response.mention_ids
        )


# pylint: disable=R0903
class MessageQueryFilter:
    """
    doc
    """
    # pylint: disable=R0913
    def __init__(
            self,
            talker_id: str = None,
            room_id: str = None,
            message_type: MessageType = None,
            to_id: str = None,
            text: str = None):
        """
        initialization
        """
        self.talker_id = talker_id
        self.room_id = room_id
        self.to_id = to_id
        self.text = text
        self.type = message_type
