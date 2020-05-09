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
from typing import Optional


@dataclass
class PuppetOptions:
    """
    option to config puppet
    """
    token: Optional[str] = None
    end_point: Optional[str] = None
    timeout: Optional[str] = None


CHAT_EVENT_DICT = {
    'friendship': 'receive a friend request',
    'login': 'puppet had logined',
    'logout': 'puppet had logouted',
    'message': 'received a new message',
    'room-invite': 'received a room invitation',
    'room-join': 'be added to a room',
    'room-leave': 'leave or be removed from a room',
    'room-topic': 'room topic had been changed',
    'scan': 'a QR Code scan is required'
}

ChatEventName = CHAT_EVENT_DICT.keys()

PUPPET_EVENT_DICT = {
    'dong': 'emit this event if you received a ding() call',
    'error': 'emit an Error instance when there\'s any Error need to '
             'report to Wechaty',
    'heart-beat': 'feed the watchdog by emit this event',
    'ready': 'emit this event after the puppet is ready(you define it)',
    'reset': 'reset the puppet by emit this event'
}
PUPPET_EVENT_DICT.update(CHAT_EVENT_DICT)

PuppetEventName = PUPPET_EVENT_DICT.keys()

