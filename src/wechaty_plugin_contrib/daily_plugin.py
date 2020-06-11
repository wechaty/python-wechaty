"""daily plugin"""
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler     # type: ignore

from wechaty import Wechaty
from wechaty.plugin import WechatyPlugin


class DailyPlugin(WechatyPlugin):
    """
    say something everyday, like `Daily Words`
    """
    @property
    def name(self) -> str:
        """get the name of the plugin"""
        return 'dayily'

    async def tick(self):
        """time tick for the plugin scheduler"""
        room = self.bot.Room.load('19961884194@chatroom')
        await room.ready()
        await room.say(f'i love you -> {datetime.now()}')

    async def init_plugin(self, wechaty: Wechaty):
        """init plugin"""
        await super().init_plugin(wechaty)
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.tick, 'interval', seconds=10)
        scheduler.start()
