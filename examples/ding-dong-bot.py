#!/usr/bin/env python3.8
"""doc"""
import asyncio

from wechaty import Wechaty


async def main():
    """doc"""
    print('hello')
    await asyncio.sleep(1)
    print('world')
    bot = Wechaty()
    print(await bot.name())


asyncio.run(main())
