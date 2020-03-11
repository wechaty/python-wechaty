<<<<<<< HEAD
"""doc"""
from __future__ import annotations

from .contact       import Contact
from .favorite      import Favorite
from .friendship    import Friendship
from .image         import Image
from .message       import Message
from .mini_program  import MiniProgram
from .room          import Room
from .tag           import Tag
from .url_link      import UrlLink

# Huan(202003): is that necessary to put "name" to `__all__`?
# name = 'user'

__all__ = [
    'Contact',
    'Favorite',
    'Friendship',
    'Image',
    'Message',
    'MiniProgram',
    'Room',
    'Tag',
    'UrlLink',
]
=======
# flake8: disable=F401
from .favorite import Favorite
from .contact import Contact
from .images import Image
from .mini_program import MiniProgram
from .room import Room
from .tag import Tag
from .url_link import UrlLink
>>>>>>> 6cc1c66dc0fbb9fcdf261ab98116ab74d5c0b8b6
