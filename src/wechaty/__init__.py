"""doc"""

#
# import types from wechaty_puppet
#

from wechaty_puppet import (    # type: ignore
    FileBox,
    MessageType,
    MessagePayload,

    # Contact
    ContactGender,
    ContactType,
    ContactPayload,

    # Friendship
    FriendshipType,
    FriendshipPayload,

    # Room
    RoomPayload,
    RoomMemberPayload,

    # UrlLink

    # RoomInvitation
    RoomInvitationPayload,

    # Image
    ImageType,

    # Event
    EventType,

    RoomQueryFilter,
    RoomMemberQueryFilter,
    FriendshipSearchQueryFilter,
    ContactQueryFilter,
    MessageQueryFilter,
    ScanStatus
)


from .config import (
    get_logger,
)
from .accessory import Accessory
from .plugin import (
    WechatyPlugin,
    WechatyPluginOptions
)
from .wechaty import (
    Wechaty,
    WechatyOptions,
)
from .user import (
    Contact,
    Favorite,
    Friendship,
    Image,
    Message,
    MiniProgram,
    Room,
    Tag,
    UrlLink,
)

from .version import VERSION
__version__ = VERSION

__all__ = [
    'Accessory',
    'Contact',
    'Favorite',
    'FileBox',
    'Friendship',
    'get_logger',
    'Image',
    'Message',
    'MiniProgram',
    'Room',
    'Tag',
    'UrlLink',
    'Wechaty',
    'WechatyOptions',

    'WechatyPlugin',
    'WechatyPluginOptions',

    'MessageType',
    'MessagePayload',

    # Contact
    'ContactGender',
    'ContactType',
    'ContactPayload',

    # Friendship
    'FriendshipType',
    'FriendshipPayload',

    # Room
    'RoomPayload',
    'RoomMemberPayload',

    # UrlLink

    # RoomInvitation
    'RoomInvitationPayload',

    # Image
    'ImageType',

    # Event
    'EventType',

    'ScanStatus',

    'RoomQueryFilter',
    'RoomMemberQueryFilter',
    'FriendshipSearchQueryFilter',
    'ContactQueryFilter',
    'MessageQueryFilter',
]
