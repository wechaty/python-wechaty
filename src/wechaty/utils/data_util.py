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

from typing import (
    Callable,
    Any,
    Dict,
    Iterable,
    Iterator,
    Optional,
    Type,
    TypeVar,
    MutableMapping,
    Generic
)

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class HookDict(MutableMapping[_KT, _VT], Generic[_KT, _VT]):
    """add hooks to the dict data
    """
    def __init__(
        self,
        data: Dict[_KT, _VT],
        set_item_hooks: Optional[Callable[[_KT, _VT, Dict[_KT, _VT]], None]] = None,
        default_type: Type = int,
    ):
        self._dict_data = data
        self._set_item_hooks = set_item_hooks
        self.default_type = default_type

    def __setitem__(self, key: _KT, value: Any) -> None:
        """triggered by `data[key] = value`"""
        self._dict_data[key] = value
        if self._set_item_hooks is not None:
            self._set_item_hooks(key, value, self._dict_data)

    def __getitem__(self, __k: _KT) -> _VT:
        """get item data"""
        return self._dict_data.get(__k, self.default_type())
    
    def __delitem__(self, __v: _KT) -> None:
        """del item by key"""
        del self._dict_data[__v]
    
    def __iter__(self) -> Iterator[_KT]:
        """get the iterable data of data"""
        return iter(self._dict_data)
    
    def __len__(self) -> int:
        """get the length of dict data"""
        return len(self._dict_data)

    def to_dict(self) -> dict:
        """get the source dict data"""
        return self._dict_data
