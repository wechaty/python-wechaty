"""check the weather"""
from collections import defaultdict
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler     # type: ignore

from wechaty import Message
from wechaty.plugin import WechatyPlugin


class DingDongRankPlugin(WechatyPlugin):
    """weather plugin for bot"""
    def __init__(self):
        """init the plugin"""
        super().__init__()

        self.room_data = {}
        self.interval_time = 8

        self.history_analyze = {}
        self.top_k = 10
        self.room_alias = {}

        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    @property
    def name(self) -> str:
        """get the name of the plugin"""
        return 'ding-dong-rank'

    async def on_message(self, msg: Message):
        """listen message event"""
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()

        if room is None:
            return

        if text in ['#ding', 'dong']:
            if room.room_id not in self.room_data:
                self.room_data[room.room_id] = {
                    '__status__': 'running'
                }
                await self.re_init_job(room.room_id)
        if text == '#ding':
            self.room_data[room.room_id]['__ding__'] = True

        if text == '#ding start':
            self.room_data[room.room_id] = {
                '__status__': 'running'
            }
            await room.say('#ding')
            await self.re_init_job(room.room_id)

        if text == 'dong':
            if room.room_id in self.room_data:
                self.room_data[room.room_id][from_contact.contact_id] = {
                    'id': from_contact.contact_id,
                    'time': datetime.now(),
                    'name': from_contact.name,
                }
                # refresh the scheduler job
                await self.re_init_job(room.room_id)

    async def get_room_alias(self, room_id, member_id, name):
        """get alias in room"""
        room = self.bot.Room(room_id)
        await room.ready()
        members = await room.member_all()

        if room_id not in self.room_alias:
            self.room_alias[room_id] = {}
            for member in members:
                await member.ready()
                alias = await room.alias(member)
                print('---' + alias + '---')
                if alias is None or alias == '':
                    self.room_alias[room_id][member.contact_id] = \
                        member.payload.name
                else:
                    self.room_alias[room_id][member.contact_id] = alias

        if member_id not in self.room_alias[room_id]:
            return name
        return self.room_alias[room_id][member_id]

    async def send_rank_analysis(self, room_id):
        """send rank analysis data to conversation room"""
        if room_id not in self.room_data:
            return

        # check if contains ding info
        if not self.room_data[room_id].get('__ding__', False):
            return

        bot_ids = [key for key in self.room_data[room_id].keys() if
                   not key.startswith('__')]
        dong_data = [self.room_data[room_id][bot_id] for bot_id in bot_ids]

        # sort the date
        dong_data.sort(key=lambda x: x['time'])

        if room_id not in self.history_analyze:
            self.history_analyze[room_id] = {}

        top_k_result = []
        last_timestamp = datetime(year=2000, month=1, day=1)
        top = 0
        for index, item in enumerate(dong_data):
            if item['id'] not in self.history_analyze[room_id]:
                self.history_analyze[room_id][item['id']] = defaultdict()

            self.history_analyze[room_id][item['id']][index + 1] = \
                self.history_analyze[room_id][item['id']].get(index + 1, 0) + 1
            if index <= self.top_k:
                if item['time'] > last_timestamp:
                    last_timestamp = item['time']
                    top += 1
                name = await self.get_room_alias(
                    room_id, item['id'], item['name']
                )
                top_k_result.append({
                    'id': item['id'],
                    'name': name,
                    'top': top
                })
        # send message to the room
        msg = '🔥🔥 DING-DONG Speed Ranking \n=========================\n'

        icon = {
            1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣',
            6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'
        }

        for item in top_k_result:
            if item['top'] in icon:
                msg += f'NO.{icon[item["top"]]} {item["name"]}\n'

        room = self.bot.Room.load(room_id)
        await room.ready()
        await room.say(msg)

        del self.room_data[room_id]

    async def re_init_job(self, room_id):
        """re init job, replace it if exist"""
        job_id = f'__job__{room_id}'
        now = datetime.now()

        job = self.scheduler.add_job(
            self.send_rank_analysis,
            replace_existing=True,
            id=job_id,
            trigger='date',
            next_run_time=now + timedelta(seconds=self.interval_time),
            kwargs={'room_id': room_id}
        )
        print('add job ...')
        print(job)
