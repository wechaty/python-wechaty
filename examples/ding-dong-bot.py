"""doc"""
import asyncio
from wechaty import Wechaty
from wechaty.user import Message
from wechaty_puppet import PuppetOptions
from wechaty_puppet_hostie import HostiePuppet


async def message(msg: Message):
    """back on message"""
    from_contact = msg.talker()
    text = msg.text()
    if from_contact is not None and text == 'ding':
        await from_contact.say('dong')
    print(msg)


async def do_some_thing():
    """do some thing"""
    friends = await bot.Contact.find_all()
    print(friends)
    print('dong some thing')


# puppet_options = PuppetOptions(token='your-token-here')

bot: Wechaty = None

async def main():
    """doc"""
    hostie_puppet = HostiePuppet(PuppetOptions('donut-test-user-6005'),
                                 'hostie-puppet')
    global bot
    bot = Wechaty(hostie_puppet).on('message', message)
    await bot.start()
    await do_some_thing()

asyncio.run(main())
