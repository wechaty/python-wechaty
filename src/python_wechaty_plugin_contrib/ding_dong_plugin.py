import asyncio
from threading import Thread
from typing import Union
from datetime import datetime
import requests
from wechaty import Message, Contact, Room, FileBox, Wechaty
from wechaty.plugin import WechatyPlugin
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class DingDongPlugin(WechatyPlugin):
    @property
    def name(self):
        return 'ding-dong'

    async def on_message(self, msg: Message):
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        if text == '#ding':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
            file_box = FileBox.from_url(
                'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
                'u=1116676390,2305043183&fm=26&gp=0.jpg',
                name='ding-dong.jpg')
            await conversation.say(file_box)


class DailyPlugin(WechatyPlugin):

    @property
    def name(self) -> str:
        return 'dayily'

    async def tick(self):
        while True:
            await asyncio.sleep(2)
            room = self.bot.Room.load('19961884194@chatroom')
            await room.ready()
            await room.say(f'i love you -> {datetime.now()}')

    async def init_plugin(self, wechaty: Wechaty):
        print(self.a)
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.tick, 'interval', seconds=10)
        scheduler.start()


class WeatherPlugin(WechatyPlugin):
    """weather plugin for bot"""
    @property
    def name(self) -> str:
        return 'weather'

    async def on_message(self, msg: Message):
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        if text == '今天天气如何':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            response = requests.get('https://tianqiapi.com/api?version=v61&appid=32896971&appsecret=5bR8Gs9x')
            result = response.json()
            result_msg = f'今天{result["wea"]} 最低温度{result["tem2"]}度 最高温度{result["tem1"]}度'
            await conversation.say(result_msg)



