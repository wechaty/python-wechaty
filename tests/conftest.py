from collections import defaultdict
import sys
from os.path import abspath, dirname, join

from typing import Dict, List, MutableMapping, Optional, Tuple
from uuid import uuid4
import pytest
from wechaty_grpc.wechaty.puppet import MessageType
from wechaty_puppet.puppet import Puppet
from wechaty_puppet.schemas.message import MessageQueryFilter
from wechaty_puppet.schemas.types import (
    MessagePayload,
    RoomPayload,
    ContactPayload,
    RoomMemberPayload,
)
from wechaty_puppet.schemas.puppet import PuppetOptions
from wechaty.wechaty import Wechaty, WechatyOptions  # noqa
from wechaty.fake_puppet import FakePuppet


@pytest.fixture
async def test_bot() -> Wechaty:
    """Initialize a Wechaty instance and return it"""
    puppet = FakePuppet(options=PuppetOptions())
    puppet.add_fake_contact(ContactPayload("wechaty_user", name="Wechaty User"))
    puppet.add_fake_contact(ContactPayload("fake_user", name="Fake User"))
    puppet.add_fake_contact(ContactPayload("test_user", name="Test User"))
    puppet.add_fake_room(
        RoomPayload(
            id="test_room",
            topic="test_room",
            owner_id="wechaty_user",
            member_ids=["wechaty_user", "fake_user", "test_user"],
        )
    )
    puppet.add_fake_room(
        RoomPayload(
            id="fake_room",
            topic="fake_room",
            owner_id="wechaty_user",
            member_ids=["wechaty_user", "fake_user", "test_user"],
        )
    )
    puppet.add_fake_room_members(
        "fake_room",
        [
            RoomMemberPayload("wechaty_user"),
            RoomMemberPayload("fake_user", room_alias="Fake Alias"),
            RoomMemberPayload("test_user")
        ]
    )
    puppet.add_fake_message(
        MessagePayload("no_mention", text="foo bar asd", type=MessageType.MESSAGE_TYPE_TEXT)
    )
    puppet.add_fake_message(
        MessagePayload(
            "room_no_mention",
            text="beep",
            room_id="fake_room",
            type=MessageType.MESSAGE_TYPE_TEXT,
        )
    )
    puppet.add_fake_message(
        MessagePayload(
            "room_with_mentions",
            text="@Wechaty User @Test User test message asd",
            room_id="fake_room",
            type=MessageType.MESSAGE_TYPE_TEXT,
            mention_ids=["wechaty_user", "test_user"],
        )
    )
    puppet.add_fake_message(
        MessagePayload(
            "room_with_mentions_and_alias",
            text="123123 @Wechaty User @Test User @Fake Alias kkasd",
            room_id="fake_room",
            type=MessageType.MESSAGE_TYPE_TEXT,
            mention_ids=["wechaty_user", "test_user", "fake_user"],
        )
    )
    puppet.add_fake_message(
        MessagePayload(
            "room_with_mentions_and_alias_mismatched",
            text="123123@Wechaty User @Test User @Fake User beep",
            room_id="fake_room",
            type=MessageType.MESSAGE_TYPE_TEXT,
            mention_ids=["wechaty_user", "test_user", "fake_user"],
        )
    )
    puppet.add_fake_message(
        MessagePayload(
            "room_with_text_mentions",
            text="@Wechaty User @Test User @Fake Alias beep!!",
            room_id="fake_room",
            type=MessageType.MESSAGE_TYPE_TEXT,
        )
    )

    bot = Wechaty(WechatyOptions(puppet=puppet))
    await bot.init_puppet()
    return bot
