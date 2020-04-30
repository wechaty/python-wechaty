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

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Type, TypeVar, Optional, List
import json
from wechaty_puppet.message import MessageType


T = TypeVar("T")


def make_payload(cls: T, payload: str) -> T:
    data: dict = json.loads(payload)
    for key, value in data.items():
        if hasattr(cls, key):
            setattr(cls, key, value)
    return cls


@dataclass
class ScanPayload:
    def __init__(self, payload: str):
        make_payload(self, payload)

    qrcode: str
    status: int


# pylint: disable=R0903
@dataclass
class MessagePayload:
    """
    doc
    """
    # pylint: disable=R0913
    def __init__(self, payload: str):
        """
        initialization

        :parameter
        ------------------------------------------------------
        talker_id:
            required; talker_id refer to who send the message.
        text:
            required; message content
        """
        data = json.loads(payload)
        make_payload(self, payload)
        self.message_id = data["messageId"]

    message_id: str
    type: MessageType
    talker_id: str
    text: str
    to_id: Optional[str]
    room_id: Optional[str]
    mention_ids: Optional[List[str]]
    timestamp: datetime


@dataclass
class LoginPayload:
    """
    store login_payload data
    """
    contact_id: str

    @classmethod
    def from_json(cls: Type[LoginPayload], data: str) -> LoginPayload:
        json_data = json.loads(data)
        if 'contactId' not in json_data:
            raise AttributeError('LoginPayload data is invalid')

        return LoginPayload(contact_id=json_data['contactId'])

