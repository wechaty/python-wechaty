"""
Unit test
"""
import pytest
from typing import Type
from typing import Optional
from wechaty.user.room import Room, RoomPayload
from wechaty.exceptions import WechatyAccessoryBindingError


def test_multi_room_instance():
    FirstRoom = Room.cloned_class('11') 
    SecondRoom = Room.cloned_class('22')

    first_room = FirstRoom('room-id')
    first_room._payload = RoomPayload(topic='first-room')

    second_room = SecondRoom('room-id')
    second_room._payload = RoomPayload(topic='second-room')
   
    assert first_room.get_puppet() == '11'
    assert str(first_room).startswith('Room')
    
    assert second_room.get_puppet() == '22'
    assert str(second_room).startswith('Room')

    with pytest.raises(WechatyAccessoryBindingError):
        Room('room-id')
