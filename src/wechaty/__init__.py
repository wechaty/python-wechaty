"""doc"""
from wechaty_puppet import (
    FileBox,
)
from .wechaty import (
    Wechaty
)

# Huan(202003): is that necessary to put "name" to `__all__`?
name = 'wechaty'

__all__ = [
    'FileBox',
    'Wechaty',
]
