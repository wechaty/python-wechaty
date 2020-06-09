"""basic ding-dong bot for the wechaty plugin"""
from typing import Union

from wechaty import Message, Contact, Room, FileBox
from wechaty.plugin import WechatyPlugin


class DingDongPlugin(WechatyPlugin):
    """basic ding-dong plugin"""
    @property
    def name(self):
        """name of the plugin"""
        return 'ding-dong'

    async def on_message(self, msg: Message):
        """listen message event"""
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
