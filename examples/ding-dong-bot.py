"""doc"""
import asyncio
from typing import Optional, Union
import logging
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from wechaty_puppet import PuppetOptions, FileBox
from wechaty_puppet_hostie import HostiePuppet


logging.basicConfig(level=logging.INFO, filename='./log.txt')
log = logging.getLogger("DingDongBot")


async def message(msg: Message):
    """back on message"""
    log.info(msg)
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
    if text == '#ding':
        conversationer: Union[
            Room, Contact] = from_contact if room is None else room
        await conversationer.ready()
        await conversationer.say('dong')
        # await conversationer.say('🤔')
        # file_box = FileBox.from_url(
        #     'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
        #     'u=1116676390,2305043183&fm=26&gp=0.jpg',
        #     name='ding-dong.jpg')
        # await conversationer.say(file_box)


async def do_some_thing():
    """do some thing"""
    friends = await bot.Contact.find_all()
    log.info(friends)

# puppet_options = PuppetOptions(token='your-token-here')

bot: Optional[Wechaty] = None


async def main():
    """doc"""
    token = open('../token.txt').readlines()[0]
    hostie_puppet = HostiePuppet(PuppetOptions(token))
    # pylint: disable=W0603
    global bot
    bot = Wechaty(hostie_puppet).on('message', message)
    await bot.start()
    await do_some_thing()


asyncio.run(main())
