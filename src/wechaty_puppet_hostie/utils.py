"""
doc
"""
from dataclasses import is_dataclass


def get_common_attributes(response: dict, payload) -> dict:
    """
    get common attributes
    :param response:
    :param payload:
    :return:
    """
    if not is_dataclass(payload):
        raise TypeError('params payload should be a dataclass type')
    common_attributes: dict = {}
    for key in payload.__dataclass_fields__.keys():
        if key in response:
            common_attributes[key] = response.get(key, None)
    return common_attributes
