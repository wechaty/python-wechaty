#!/usr/bin/env python3.8
"""doc"""
import asyncio

from wechaty import FileBox


async def main():
    """doc"""
    print('hello')
    await asyncio.sleep(1)
    print('world')
    f = FileBox()
    print(await f.to_file('t.dat'))


asyncio.run(main())
