"""
doc
"""

# message module
from chatie_grpc.wechaty import (   # type: ignore

    # Message
    MessageType,
    MessagePayloadResponse as MessagePayload,

    # Contact
    ContactGender,
    ContactType,
    ContactPayloadResponse as ContactPayload,

    # Message
    # Friendship
    FriendshipType,
    FriendshipPayloadResponse as FriendshipPayload,

    # Room
    RoomPayloadResponse as RoomPayload,
    RoomMemberPayloadResponse as RoomMemberPayload,

    # UrlLink

    # RoomInvitation
    RoomInvitationPayloadResponse as RoomInvitationPayload,

    # Image
    ImageType,

    # Event
    EventType,

    # MiniProgram

    # MessageContactResponse,
    # MessageFileResponse,
    # MessageImageResponse
)

from .puppet import (
    Puppet,
    PuppetOptions
)
from .file_box import FileBox

from .schemas.message import (
    MessageQueryFilter,
)

from .schemas.contact import (
    ContactQueryFilter
)

from .schemas.friendship import (
    FriendshipSearchCondition
)

from .schemas.room import (
    RoomQueryFilter,
    RoomMemberQueryFilter,
)

from .schemas.url_link import UrlLinkPayload

from .schemas.mini_program import MiniProgramPayload

from .schemas.event import (
    EventScanPayload,
    ScanStatus,

    EventDongPayload,
    EventLoginPayload,
    EventReadyPayload,
    EventLogoutPayload,
    EventResetPayload,

    EventRoomTopicPayload,
    EventRoomLeavePayload,
    EventRoomJoinPayload,
    EventRoomInvitePayload,


    EventMessagePayload,
    EventHeartbeatPayload,
    EventFriendshipPayload,
    EventErrorPayload
)

__all__ = [
    'Puppet',
    'PuppetOptions',

    'ContactGender',
    'ContactPayload',
    'ContactQueryFilter',
    'ContactType',

    'FileBox',
    'FriendshipType',
    'FriendshipSearchCondition',
    'FriendshipPayload',

    'MessagePayload',
    'MessageQueryFilter',
    'MessageType',

    'UrlLinkPayload',

    'RoomQueryFilter',
    'RoomPayload',
    'RoomMemberQueryFilter',
    'RoomMemberPayload',

    'RoomInvitationPayload',

    'MiniProgramPayload',

    'EventScanPayload',
    'ScanStatus',

    'EventDongPayload',
    'EventLoginPayload',
    'EventReadyPayload',
    'EventLogoutPayload',
    'EventResetPayload',
    'EventFriendshipPayload',
    'EventHeartbeatPayload',
    'EventMessagePayload',
    'EventRoomInvitePayload',
    'EventRoomJoinPayload',
    'EventRoomLeavePayload',
    'EventRoomTopicPayload',
    'EventErrorPayload',

    'ImageType',
    'EventType'

]
