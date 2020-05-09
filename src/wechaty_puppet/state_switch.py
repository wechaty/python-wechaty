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
from typing import Optional, Union


class StateType(Enum):
    """
    state type
    """
    On = 0
    Off = 1
    Pending = 2


class StateSwitch:
    """
    puppet state switcher
    """
    def __init__(self, name: Optional[str] = None):
        self.name: Optional[str] = name
        self._state = StateType.Off

    def on(self, state: Optional[Union[bool, StateType]] = None
           ) -> Union[bool, StateType]:
        """
        Turn on the current state.
        """
        if state is None:
            if self._state == StateType.On:
                return True
            return self._state

        if isinstance(state, bool):
            if not state:
                raise ValueError(
                    'when set on state, bool value should be True')

            self._state = StateType.On
            return True
        if isinstance(state, StateType):
            if state != StateType.Pending:
                raise ValueError(
                    f'state StateType value <{state}> should be Pending')
            self._state = StateType.Pending
            return state
        raise ValueError(
            'state params type is only for [bool, StateType]')

    def off(self, state: Optional[Union[bool, StateType]] = None
            ) -> Union[bool, StateType]:
        """
        Turn Off the current state
        """
        if state is None:
            if self._state == StateType.Off:
                return True
            return self._state

        if isinstance(state, bool):
            if not state:
                raise ValueError(
                    'when set off state, bool value should be False')
            self._state = StateType.On
            return True
        if isinstance(state, StateType):
            if state != StateType.Pending:
                raise ValueError(
                    f'state StateType value <{state}> should be Pending')
            self._state = StateType.Pending
            return state
        raise ValueError(
            'state params type is only for [bool, StateType]')
