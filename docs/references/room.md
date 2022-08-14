---
title: Room
---

> 微信群聊（组）的相关功能被封装在 `Room` 类中。
> 
> [示例/Room-Bot](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/advanced/room_bot.py)

::: wechaty.user.room.Room.on
### 示例代码 (EVENT:JOIN)
```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("event-room") # 把`event-room`改为您在微信中加入的任意群聊的群聊名称

async def on_join(invitees, inviter):
    log.info('Bot' + 'EVENT: room-join - Room "%s" got new member "%s", invited by "%s"' %
                 (await room.topic(), ','.join(map(lambda c: c.name, invitees)), inviter.name))

if room:
    room.on('join', on_join)
```
### 示例代码 (EVENT:LEAVE)
```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("event-room") # 把`event-room`改为您在微信中加入的任意群聊的群聊名称

async def on_leave(leaver_list, remover):
    log.info('Bot' + '群聊事件: 离开 - "%s" leave(remover "%s"), bye bye' % (','.join(leaver_list), remover or 'unknown'))

if room:
    room.on('leave', on_leave)

```
### 示例代码 (EVENT:TOPIC)
```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("wechaty") # 把`wechaty`改为您在微信中加入的任意群聊的群聊名称

async def on_topic(topic, old_topic, changer):
    log.info('Bot' + 'Room EVENT: topic - changed from "%s" to "%s" by member "%s"' % (old_topic, topic, changer.name()))

if room:
    room.on('topic', on_topic)
```
### 示例代码 (EVENT:INVITE)
```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("wechaty") # 把`wechaty`改为您在微信中加入的任意群聊的群聊名称

async def on_invite(room_invitation):
    room_invitation.accept()

if room:
    room.on('invite', on_invite)
```
### RoomEventName

群聊类的事件类型(Room Class Event Type)

**类型**: 全局类型定义 

**属性**

| 名称 | 类型 | 描述 |
| :--- | :--- | :--- |
| join | `str` | 当有人进入群聊时触发. |
| topic | `str` | 获取群名事件, 当有人改变群聊名称时候 |
| leave | `str` | 当有人退出群聊时触发. <br/>`注意: 如果有人自己退出群聊，微信不会提醒房间里的其他人，所以机器人在此情况不会收到“leave”事件`。 |
| invite | `str` | 当有人被邀请入群是触发 |


### RoomEventFunction
群聊事件函数, 供开发者重写

**类型**: 全局类型定义 

**属性**

| 名称 | 类型 | 参数 | 描述| 
| :--- | :--- | :--- |:--- |
| on_room_join | `function` | \(self: Wechaty, room_invitation: RoomInvitation\); None | 有人加入群聊时触发 |
| on_room_topic | `function` | \(self: Wechaty, room: Room, new_topic: str, old_topic: str, changer: Contact, date: datetime\); None | 有人改变群聊名称时触发 |
| on_room_leave | `function` | \(self: Wechaty, room: Room, leavers: List\[Contact\],remover: Contact, date: datetime\); None | 有人被移出群聊时触发 |
| on_room_invite | `function` | \(self, room_invitation: RoomInvitation\); None | 有人邀请Bot加入群聊时触发 |

::: wechaty.user.room.Room.emit

::: wechaty.user.room.Room.create
### 示例代码
> 用联系人'lijiarui' 和 'juxiaomi'创建一个群聊, 群聊的名称为'ding - created'
```python
helper_contact_a = await bot.Contact.find('lijiarui')
helper_contact_b = await bot.Contact.find('juxiaomi')
contact_list = [helper_contact_a, helper_contact_b]
print('机器人创建所用的联系人列表为: %s', contact_list.join(','))
room = await Room.create(contact_list, 'ding')
print('Bot createDingRoom() new ding room created: %s', room)
await room.topic('ding - created')  # 设置群聊名称
await room.say('ding - 创建完成')
```

::: wechaty.user.room.Room.find_all
## RoomQueryFilter

::: wechaty.user.room.Room.find

::: wechaty.user.room.Room.load

::: wechaty.user.room.Room.ready

::: wechaty.user.room.Room.say
> 注意: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
### 示例代码
```python
from wechaty import Wechaty, FileBox, UrlLink, MiniProgram
import asyncio


class MyBot(Wechaty):
    async def on_login(self, contact: Contact):
        # 等待登入
        room = await bot.Room.find('wechaty')  # 可以根据 room 的 topic 和 id 进行查找

        # 1. 向房间发送文本
        await room.say('Hello world!')

        # 2.发送语音文件到群聊
        file_box1 = FileBox.from_url(
            url='https://wechaty.github.io/wechaty/images/bot-qr-code.png', name='QRCode')
        file_box2 = FileBox.from_file("./test.txt")  # 注意路径，以及文件不能为空
        await room.say(file_box1)
        await room.say(file_box2)

        # 3. 发送名片到群聊
        contact_card = await self.Contact.find('master')
        await room.say(contact_card)

        # 4. 在群聊内发送文本, 并提及(@) `some_members_id`列表里面提供的人
        members = await special_room.member_list()  # 房间内的所有联系人对象
        some_members_id = [m.contact_id for m in members[:3]]
        await room.say('Hello world!', some_members_id)

        # 5. 在群聊内发送连接
        urlLink = UrlLink.create(
            description='WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
            thumbnail_url='https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
            title='Welcome to Wechaty',
            url='https://github.com/wechaty/wechaty',
        )
        await room.say(urlLink)

        # 6. 发送小程序 (暂时只有`wechaty-puppet-macpro`支持该功能)
        miniProgram = self.MiniProgram.create_from_json({
            "appid": 'gh_0aa444a25adc',
            "title": '我正在使用Authing认证身份，你也来试试吧',
            "pagePath": 'routes/explore.html',
            "description": '身份管家',
            "thumbUrl": '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
            "thumbKey": '42f8609e62817ae45cf7d8fefb532e83',
        })
        await room.say(mini_program)

asyncio.run(MyBot().start())
```

::: wechaty.user.room.Room.add
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
> 请参阅[网页版微信封闭了群聊接口](https://github.com/wechaty/wechaty/issues/1441)
### 示例代码
```python
bot = Wechaty()
await bot.start()
# after logged in...
contact = await bot.Contact.find('lijiarui') # 把'lijiarui'改为您通讯录中的任意联系人
room = await bot.Room.find('wechaty')  # 把`wechaty`改为您在微信中加入的任意群聊的群聊名称
if room:
    try:
        await room.add(contact)
    except Exception  as e:
        log.error(e)
```

::: wechaty.user.room.Room.delete
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
>
> 请参阅[网页版微信封闭了群聊接口](https://github.com/wechaty/wechaty/issues/1441)
### 示例代码
```python
bot = Wechaty()
await bot.start()
# after logged in...
room = await bot.Room.find('wechat')   # change 'wechat' to any room topic in your wechat
contact = await bot.Contact.find('lijiarui')   # change 'lijiarui' to any room member in the room you just set
if room:
    try:
        await room.delete(contact)
    except Exception as e:
        log.error(e)
```

::: wechaty.user.room.Room.quit
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

::: wechaty.user.room.Room.topic
### 示例代码1
> 当任意联系人在群聊内发送消息, 您都会得到该群聊的名称

```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room: "Room" = msg.room()
        topic = await room.topic()
        print(f'群聊名: {topic}')

asyncio.run(MyBot().start())
```
### 示例代码2
> 每当机器人登陆账号时, 机器人都会改变群聊的名字。
```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        room = await bot.Room.find('your room')  # 替换为您所加入的任意群聊
        old_topic = await room.topic()
        new_topic = await room.topic('Wechaty!')
        print(f'群聊名从{old_topic}改为{new_topic}')

asyncio.run(MyBot().start())
```
::: wechaty.user.room.Room.announce
> 注意: 这个功能只有机器人是群主时才可以使用

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
### 示例代码1
> 当群聊内的任意联系人发送消息时, 您都会在控制台收到群公告的内容
```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room: "Room" = msg.room()
        announce = await room.announce()
        print(f'群公告为: {announce}')

asyncio.run(MyBot().start())
```

### 示例代码2
> 每当机器人登陆账号时, 都会改变群聊公告的内容
```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        room = await bot.Room.find('your room')  # 替换为您所加入的任意群聊
        old_announce = await room.announce()
        new_announce = await room.announce('改变为wechaty!')
        print(f'群聊的公告从{old_announce}改变为{new_announce}')

asyncio.run(MyBot().start())
```

::: wechaty.user.room.Room.qr_code
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

::: wechaty.user.room.Room.alias
### 示例代码
```python
room = await bot.Room.find('your room')  # 要发送消息的群聊名
contact = await bot.Contact.find('lijiarui')  # 找到目标联系人
alias = await room.alias(contact)  # 获取该联系人的备注(别名)
print(f'{contact.name()}的别名是{alias}')
```

::: wechaty.user.room.Room.has
### 示例代码
> 检查联系人 'lijiarui'是否在群聊'wechaty'内
```python
contact = await bot.Contact.find('lijiarui')
room = await bot.Room.find('wechaty')
if contact and room:
    if await room.has(contact):
        print(f'{contact.name()} 在群聊wechaty房间内!')
    else:
        print(f'{contact.name()} 不在群聊wechaty房间内!')
```

::: wechaty.user.room.Room.member_list
### 示例代码
```python
member_list = await room.member_list()
print(f'room all member list: {member_list}')

member_contact_list = await room.member_list('abc')
print(f'contact list with all name, room alias, alias are abc: {member_contact_list}')
```

::: wechaty.user.room.Room.member
### 示例代码1
> 通过名字寻找联系人
```python
room = await bot.Room.find('wechaty')
if room:
    member = await room.member('lijiarui')
    if member:
        print(f'wechaty 群聊内找到了联系人: {member.name()}')
    else:
        print(f'wechaty群聊内找不到该联系人')
```
### 示例代码2
> 通过MemberQueryFilter类来查找
```python
import asyncio
from wechaty import Wechaty, Room, Message
from wechaty_puppet.schemas.room import RoomMemberQueryFilter

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room: "Room" = msg.room()
        if room:
            member = await room.member(RoomMemberQueryFilter(name="lijiarui"))
            if member:
                print(f'wechaty room got the member: {member.name}')
            else:
                print(f'cannot get member in wechaty room!')


asyncio.run(MyBot().start())
```
### RoomMemberQueryFilter
寻找群成员的一种方法Room.member\(\)

**类型**: 全局类型定义 

**属性**

| 名称 | 类型 | 描述 |
| :--- | :--- | :--- |
| name | `string` | 由联系人自身设置的名字, 叫做`name`, 等同于`Contact.name()`. |
| roomAlias | `string` | 由联系人自身在群聊内设置的群别名\(备注, 昵称\), 叫做群昵称`roomAlias` |
| contactAlias | `string` | 由机器人为联系人设置的备注\(别名\), 叫做联系人备注`alias`, 等同于 `Contact.alias()`. 详见[issues#365](https://github.com/wechaty/wechaty/issues/365) |


::: wechaty.user.room.Room.owner
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)


::: wechaty.user.room.Room.avatar
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)