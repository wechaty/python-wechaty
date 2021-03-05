"""doc"""
# pylint: disable=R0801
import asyncio
import logging
from typing import List, Optional, Union

from wechaty_puppet import FileBox  # type: ignore
from wechaty_puppet.schemas.event import EventReadyPayload  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        """initialization function
        """
        super().__init__()

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        if text == '#ding':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
            file_box = FileBox.from_url(
                'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
                'u=1116676390,2305043183&fm=26&gp=0.jpg',
                name='ding-dong.jpg')
            await conversation.say(file_box)

    async def on_login(self, contact: Contact):
        """login event

        Args:
            contact (Contact): the account logined
        """
        print('user: %s has login', contact)

    async def on_ready(self, payload: EventReadyPayload):
        """all initialization jobs should be done here.

        eg: get all of friends/rooms/room-members

        Args:
            payload (EventReadyPayload): the data of ready event
        """
        log.info('ready event <%s>', payload)
        # 1. get all of friends
        friends: List[Contact] = await self.Contact.find_all()
        for friend in friends:
            log.info('load friend<%s>', friend)

        # 2. get all of rooms
        rooms: List[Room] = await self.Room.find_all()
        for room in rooms:
            log.info('load room<%s>', room)


bot: Optional[MyBot] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = MyBot()
    await bot.start()


asyncio.run(main())
