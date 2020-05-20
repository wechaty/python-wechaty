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
from collections import defaultdict
from enum import Enum
from typing import Union
from datetime import datetime, timedelta


class OperationType(Enum):
    Equal = 0
    StartsWith = 1
    EndsWith = 2
    Contains = 3


class BaseField:
    """
    TODO -> target function example code:

    result = bot.Contact.search(ContactFilter.id == 'wexin_id')

    result = bot.Contact.search(id == 'wexin_id')

    I think that this way may be a best practice for search.

    """
    def __init__(self):
        self._operation_pool = defaultdict()

    def _add_operation(self, field_name: str, operation_type: OperationType,
                       value: Union[str, int]):
        """
        internal operation save
        :param field_name:
        :param operation_type:
        :param value:
        :return:
        """
        pass


class StringField(BaseField, str):
    """
    string field for filter
    """
    def __init__(self, value: str):
        super().__init__()


class IntegerField(BaseField, int):
    """
    integer field for filter
    """
    def __init__(self, value: int):
        super().__init__()


class FloatField(BaseField, float):
    """
    float field for filter
    """
    def __init__(self, value: float):
        super().__init__()


class DataTimeField(BaseField, datetime):
    """
    datetime field for filter
    """
    def __init__(self, value: datetime):
        super().__init__()


class TimeStampField(BaseField, timedelta):
    """
    timedelta/timestamp field for filter
    """
    def __init__(self, value: timedelta):
        super().__init__()


class BoolField(BaseField, bool):
    """
    bool filed for field
    """
    def __init__(self, value: bool):
        super().__init__()
