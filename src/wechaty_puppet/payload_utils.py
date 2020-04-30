"""doc"""

from __future__ import annotations

from typing import TypeVar
from dataclasses import is_dataclass

T = TypeVar("T")


def init_payload(payload: T, response) -> T:
    """
    init payload from response automatically
    :param payload:
    :param response:
    :return:
    """
    if is_dataclass(payload):
        payload_dict_data = payload.__dict__
        for key in payload_dict_data.keys():
            if hasattr(response, key):
                value = getattr(response, key)
                setattr(payload, key, value)
    return payload
