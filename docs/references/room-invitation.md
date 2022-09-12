---
title: RoomInvitation
---

> 对群聊邀请事件的封装

::: wechaty.user.room_invitation.RoomInvitation.load

::: wechaty.user.room_invitation.RoomInvitation.accept
### 示例代码
```python
import asyncio
from wechaty import Wechaty, RoomInvitation


class MyBot(Wechaty):

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        try:
            print("收到群聊邀请事件")
            await room_invitation.accept()
            print("已经自动接受")
        except Exception as e:
            print(e)

asyncio.run(MyBot().start())
```

::: wechaty.user.room_invitation.RoomInvitation.inviter
### 示例代码
```python
import asyncio
from wechaty import Wechaty, RoomInvitation


class MyBot(Wechaty):

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        try:
            print("收到群聊邀请事件")
            inviter = await room_invitation.inviter()
            inviter_name = inviter.name
            print(f"收到来自{inviter_name}的群聊邀请")
        except Exception as e:
            print(e)

asyncio.run(MyBot().start())
```

::: wechaty.user.room_invitation.RoomInvitation.topic
### 示例代码
```python
import asyncio
from wechaty import Wechaty, RoomInvitation


class MyBot(Wechaty):

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        try:
            room_name = await room_invitation.topic()
            print(f"收到来自{room_name}的群聊邀请")
        except Exception as e:
            print(e)

asyncio.run(MyBot().start())
```

::: wechaty.user.room_invitation.RoomInvitation.member_count

::: wechaty.user.room_invitation.RoomInvitation.member_list

::: wechaty.user.room_invitation.RoomInvitation.date

::: wechaty.user.room_invitation.RoomInvitation.age
> 举个例子, 有条群聊邀请是`8:43:01`发送的, 而当我们在Wechaty中接收到它的时候时间已经为 `8:43:15`, 那么这时 `age()`返回的值为 `8:43:15 - 8:43:01 = 14 (秒)`

::: wechaty.user.room_invitation.RoomInvitation.from_json

::: wechaty.user.room_invitation.RoomInvitation.to_json