"""doc"""
import asyncio
import logging
from typing import Optional, Union

from wechaty_puppet import PuppetOptions, FileBox  # type: ignore

from wechaty import Wechaty, Contact, WechatyOptions
from wechaty.user import Message, Room

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='./log.txt'
)
log = logging.getLogger(__name__)


async def message(msg: Message):
    """back on message"""
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

bot: Optional[Wechaty] = None


async def main():
    """doc"""
    token = open('../token.txt').readlines()[0]
    token = token.replace('\n', '')
    # pylint: disable=W0603
    global bot
    options = WechatyOptions(
        puppet='wechaty-puppet-hostie',
        puppet_options=PuppetOptions(
            token=token
        )
    )
    bot = Wechaty(options).on('message', message)
    await bot.start()


asyncio.run(main())
