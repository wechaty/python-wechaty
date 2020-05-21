"""doc"""
import asyncio
import logging
from typing import Optional, Union

from wechaty_puppet import PuppetOptions    # type: ignore
from wechaty_puppet_hostie import HostiePuppet  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger('DingDongBot')


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
        # content = open('log.txt', 'rb').read()
        # base64_str = base64.b64encode(content)
        # file_box = FileBox.from_file('ding-dong-icon.png', name='ding-dong.png')
        # file_box = FileBox.from_base64(base64=base64_str, name='log.txt')
        # file_box = FileBox.from_base64(base64=base64_str, name='log.txt')
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
    token = token.replace('\n', '')
    hostie_puppet = HostiePuppet(PuppetOptions(token))
    # pylint: disable=W0603
    global bot
    bot = Wechaty(hostie_puppet).on('message', message)
    await bot.start()


asyncio.run(main())
