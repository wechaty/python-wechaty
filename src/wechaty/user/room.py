"""
python-implementation for room
"""
from __future__ import annotations

# from threading import Event, Thread
from ..accessory import Accessory


class Room(Accessory):
    """docs"""

    def __init__(self, room_id: str) -> None:
        """docs"""
        self.room_id = room_id

    async def quit(self) -> None:
        """docs"""
