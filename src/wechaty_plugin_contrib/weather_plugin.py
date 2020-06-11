"""check the weather"""
from typing import Union

import requests

from wechaty import Message, Contact, Room
from wechaty.plugin import WechatyPlugin


class WeatherPlugin(WechatyPlugin):
    """weather plugin for bot"""
    @property
    def name(self) -> str:
        """get the name of the plugin"""
        return 'weather'

    async def on_message(self, msg: Message):
        """listen message event"""
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        if text == '今天天气如何':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            response = requests.get('https://tianqiapi.com/api?version=v61&'
                                    'appid=32896971&appsecret=5bR8Gs9x')
            result = response.json()
            result_msg = f'今天{result["wea"]} 最低温度{result["tem2"]}度 ' \
                         f'最高温度{result["tem1"]}度'
            await conversation.say(result_msg)
