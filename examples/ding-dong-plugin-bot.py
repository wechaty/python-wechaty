"""doc"""
import asyncio
from typing import Optional
from wechaty import Wechaty
from python_wechaty_plugin_contrib import (
    DingDongPlugin, WeatherPlugin
)
from python_wechaty_plugin_contrib.ding_dong_rank_plugin import DingDongRankPlugin

bot: Optional[Wechaty] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = Wechaty().use([DingDongPlugin(), WeatherPlugin(), DingDongRankPlugin()])
    # await bot.stop()
    await bot.start()

asyncio.run(main())
