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
from datetime import datetime


class MessageType(Enum):
    """
    doc
    * - MessageType.Unknown     </br>
    * - MessageType.Attachment  </br>
    * - MessageType.Audio       </br>
    * - MessageType.Contact     </br>
    * - MessageType.Emoticon    </br>
    * - MessageType.Image       </br>
    * - MessageType.Text        </br>
    * - MessageType.Video       </br>
    * - MessageType.Url         </br>
    """
    Unknown = 0
    Attachment = 1
    Audio = 2
    Contact = 3
    Emoticon = 4
    Image = 5
    Text = 6
    Video = 7
    Url = 8
    Recalled = 9
    MiniProgram = 10


# pylint: disable=R0903
class MessagePayload:
    """
    doc
    """
    # pylint: disable=R0913
    def __init__(
            self,
            talker_id: str,
            text: str,
            to_id: str = None,
            room_id: str = None,
            message_type: MessageType = MessageType.Unknown,
            mention_ids: List[str] = None):
        """
        initialization

        :parameter
        ------------------------------------------------------
        talker_id:
            required; talker_id refer to who send the message.
        text:
            required; message content
        """
        self.type: MessageType = message_type

        self.talker_id: str = talker_id
        self.text: str = text
        self.to_id: Optional[str] = to_id
        self.room_id: Optional[str] = room_id
        self.mention_ids: Optional[List[str]] = mention_ids
        self.timestamp: datetime = datetime.now()


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
