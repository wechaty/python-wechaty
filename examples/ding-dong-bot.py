"""doc"""
import asyncio
from wechaty import Wechaty
from wechaty.user import Message


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

bot = Wechaty(token='donut-test-user-6005').on('message', message)


async def main():
    """doc"""
    await bot.start()
    await do_some_thing()

asyncio.run(main())
