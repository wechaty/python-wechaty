"""doc"""
from .qr_code import qr_terminal
from .type_check import default_str
from .date_util import timestamp_to_date
from .data_util import WechatySetting
# from .type_check import type_check

__all__ = [
    'qr_terminal',
    'default_str',
    'timestamp_to_date',
    'WechatySetting'
    # 'type_check'
]
