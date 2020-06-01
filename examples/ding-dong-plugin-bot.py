"""doc"""
import asyncio
from typing import Optional
from wechaty import Wechaty
from python_wechaty_plugin_contrib import (
    DingDongPlugin, DailyPlugin, WeatherPlugin
)


bot: Optional[Wechaty] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = Wechaty().use([DingDongPlugin(), DailyPlugin(), WeatherPlugin()])
    await bot.start()


asyncio.run(main())
