---
title: Friendship
---

发送、接收好友请求和好友确认事件。

## Friendship

发送、接收好友请求和好友确认事件。

1. 发送请求
2. 接收请求\(in friend event\)
3. 接受请求\(friend event\)

[示例/Friend-Bot](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/advanced/friendship-bot.py)

**类型**: 全局类

* [Friendship](friendship.md#Friendship)
  * _实例方法_
    * [.accept\(\)](friendship.md#Friendship+accept) ⇒ `None`
    * [.hello\(\)](friendship.md#Friendship+hello) ⇒ `str`
    * [.contact\(\)](friendship.md#Friendship+contact) ⇒ `Contact`
    * [.type\(\)](friendship.md#Friendship+type) ⇒ `FriendshipType`
  * _静态方法_
    * [~~.send\(\)~~](friendship.md#Friendship.send)
    * [.add\(contact, hello\)](friendship.md#Friendship.add) ⇒ `None`

### friendship.accept\(\) ⇒ `None`

接受朋友请求

**类型**: [`Friendship`](friendship.md#Friendship)的实例方法  

#### 示例

```python
import asyncio
from wechaty import Wechaty, Friendship


class MyBot(Wechaty):

    async on_friendship(self, friendship: Friendship) -> None:
        contact = friendship.contact()
        await contact.ready()

        if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE:
            log_msg = 'accepted automatically'
            await friendship.accept()
            # if want to send msg, you need to delay sometimes

            print('waiting to send message ...')
            await asyncio.sleep(3)
            await contact.say('hello from wechaty ...')
            print('after accept ...')
        elif friendship.type() == FriendshipType.FRIENDSHIP_TYPE_CONFIRM:
            log_msg = 'friend ship confirmed with ' + contact.name

        print(log_msg)

asyncio.run(MyBot().start())
```

### friendship.hello\(\) ⇒ `str`

Get verify message from

**类型**: [`Friendship`](friendship.md#Friendship)的实例方法  

**示例** 

_\(If request content is \`ding\`, then accept the friendship\)_

```python
import asyncio
from wechaty import Wechaty, Friendship


class MyBot(Wechaty):

    async on_friendship(self, friendship: Friendship) -> None:
        contact = friendship.contact()
        await contact.ready()

        if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE and friendship.hello() == 'ding':
            log_msg = 'accepted automatically because verify messsage is "ding"'
            await friendship.accept()
            # if want to send msg, you need to delay sometimes

            print('waiting to send message ...')
            await asyncio.sleep(3)
            await contact.say('hello from wechaty ...')
            print('after accept ...')

asyncio.run(MyBot().start())
```

### friendship.contact\(\) ⇒ `Contact`

获取邀请的联系人对象

**类型**: [`Friendship`](friendship.md#Friendship)的实例方法  

#### 示例

```python
import asyncio
from wechaty import Wechaty, Friendship


class MyBot(Wechaty):

    async on_friendship(self, friendship: Friendship) -> None:
        contact = friendship.contact()
        await contact.ready()
        log_msg = f'receive "friendship" message from {contact.name}'
        print(log_msg)


asyncio.run(MyBot().start())
```

### friendship.type\(\) ⇒ `FriendshipType`

返回Friendship请求的类型

> 提示: FriendshipType在这里是枚举类型. &lt;/br&gt;
>
> * FriendshipType.FriendshipTypeFRIENDSHIP_TYPE_UNSPECIFIED
> * FriendshipType.FRIENDSHIP_TYPE_CONFIRM 
> * FriendshipType.FRIENDSHIP_TYPE_RECEIVE 
> * FriendshipType.FRIENDSHIP_TYPE_VERIFY 

**类型**: [`Friendship`](friendship.md#Friendship)的实例方法  

**示例** _\(If request content is \`ding\`, then accept the friendship\)_

```python
import asyncio
from wechaty import Wechaty, Friendship


class MyBot(Wechaty):

    async on_friendship(self, friendship: Friendship) -> None:
        contact = friendship.contact()
        await contact.ready()

        if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE and friendship.hello() == 'ding':
            log_msg = 'accepted automatically because verify messsage is "ding"'
            await friendship.accept()
            # if want to send msg, you need to delay sometimes

            print('waiting to send message ...')
            await asyncio.sleep(3)
            await contact.say('hello from wechaty ...')
            print('after accept ...')

asyncio.run(MyBot().start())
```

### ~~Friendship.send\(\)~~

_**已弃用**_

请使用[Friendship\#add](friendship.md#friendship-add-contact-hello-promise)

**类型**:  [`Friendship`](friendship.md#Friendship)的静态方法

### Friendship.add\(contact, hello\) ⇒ `Promise <void>`

Send a Friend Request to a `contact` with message `hello`.

The best practice is to send friend request once per minute. Remeber not to do this too frequently, or your account may be blocked.

**类型**:  [`Friendship`](friendship.md#Friendship)的静态方法

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| contact | `Contact` | Send friend request to contact |
| hello | `string` | The friend request content |

#### Example

```python
memberList = await room.memberList()
for member in memberList:
    await bot.Friendship.add(member, 'Nice to meet you! I am wechaty bot!')

```
