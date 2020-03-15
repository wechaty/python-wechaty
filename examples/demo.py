#!/usr/bin/env python3.8
"""doc"""
import asyncio

from wechaty import Wechaty


async def main():
    """doc"""
    print('hello')
    await asyncio.sleep(1)
    bot = Wechaty()
    name = await bot.name()
    print(name)
    print('world')


asyncio.run(main())
