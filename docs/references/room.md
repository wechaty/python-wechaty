---
title: Room
---

# Table of Contents

* [wechaty.user.Room](#wechaty.user.Room)
  * [Room](#wechaty.user.room.Room)
    * [\_\_init\_\_](#wechaty.user.room.Room.__init__)
    * [on](#wechaty.user.room.Room.on)
    * [emit](#wechaty.user.room.Room.emit)
    * [create](#wechaty.user.room.Room.create)
    * [find\_all](#wechaty.user.room.Room.find_all)
    * [find](#wechaty.user.room.Room.find)
    * [load](#wechaty.user.room.Room.load)
    * [\_\_str\_\_](#wechaty.user.room.Room.__str__)
    * [ready](#wechaty.user.room.Room.ready)
    * [say](#wechaty.user.room.Room.say)
    * [add](#wechaty.user.room.Room.add)
    * [delete](#wechaty.user.room.Room.delete)
    * [quit](#wechaty.user.room.Room.quit)
    * [topic](#wechaty.user.room.Room.topic)
    * [announce](#wechaty.user.room.Room.announce)
    * [qr\_code](#wechaty.user.room.Room.qr_code)
    * [alias](#wechaty.user.room.Room.alias)
    * [has](#wechaty.user.room.Room.has)
    * [member\_list](#wechaty.user.room.Room.member_list)
    * [member](#wechaty.user.room.Room.member)
    * [owner](#wechaty.user.room.Room.owner)
    * [avatar](#wechaty.user.room.Room.avatar)

<a name="wechaty.user.Room"></a>
# wechaty.user.Room

<a name="wechaty.user.room.Room"></a>
## Room Objects

```python
class Room(Accessory[RoomPayload])
```

所有的微信群，都会用一个 Room 对象封装。

<a name="wechaty.user.room.Room.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(room_id: str) -> None
```
构造函数。

<a name="wechaty.user.room.Room.on"></a>
#### on

```python
 | on(event_name: str, func)
```
捕获事件。

<a name="wechaty.user.room.Room.emit"></a>
#### emit

```python
 | emit(event_name: str, *args, **kwargs)
```
触发一个事件。

<a name="wechaty.user.room.Room.create"></a>
#### create

```python
 | @classmethod
 | async create(cls, contacts: List[Contact], topic: str) -> Room
```

使用该方法创建一个新群，需要传入群成员的列表，方法会返回一个 Room 实例。发生错误的时候，会产生 WechatyOperationError 错误。

<a name="wechaty.user.room.Room.find_all"></a>
#### find\_all

```python
 | @classmethod
 | async find_all(cls, query: Union[str, RoomQueryFilter] = None) -> List[Room]
```
静态方法，根据查询条件返回群列表，查询条件可以是关键字，可以是一个 RoomQueryFilter 对象。

<a name="wechaty.user.room.Room.find"></a>
#### find

```python
 | @classmethod
 | async find(cls, query: Union[str, RoomQueryFilter] = None) -> Union[None, Room]
```

静态方法，根据查询条件返回一个群，查询条件可以是关键字，可以是一个 RoomQueryFilter 对象。如果有多个符合条件的结果，返回第一个。

<a name="wechaty.user.room.Room.load"></a>
#### load

```python
 | @classmethod
 | load(cls, room_id: str) -> Room
```
静态方法，根据 room_id，加载一个群对象。这个群会被缓存起来。

<a name="wechaty.user.room.Room.__str__"></a>
#### \_\_str\_\_

```python
 | __str__()
```
该方法定义了群对象作为字符串的表示方法（方便 print）。

<a name="wechaty.user.room.Room.ready"></a>
#### ready

```python
 | async ready(force_sync=False)
```

内部私有方法，不建议程序员使用此方法。

<a name="wechaty.user.room.Room.say"></a>
#### say

```python
 | async say(some_thing: Union[str, Contact,
 |                                     FileBox, MiniProgram, UrlLink], mention_ids: Optional[List[str]] = None) -> Union[None, Message]
```

在群里发送消息，可以发送的消息类型有：
 * Contact 名片
 * FileBox 文件
 * MiniProgram 小程序
 * UrlLink 链接

发送的消息可以 @ 用户，使用 id 列表传入。

<a name="wechaty.user.room.Room.add"></a>
#### add

```python
 | async add(contact: Contact)
```

邀请人加入群聊。

<a name="wechaty.user.room.Room.delete"></a>
#### delete

```python
 | async delete(contact: Contact)
```
从群聊中踢人。需要管理员权限。

<a name="wechaty.user.room.Room.quit"></a>
#### quit

```python
 | async quit()
```
退出群聊。

<a name="wechaty.user.room.Room.topic"></a>
#### topic

```python
 | async topic(new_topic: str = None) -> Optional[str]
```
获取或设置群聊的标题。

<a name="wechaty.user.room.Room.announce"></a>
#### announce

```python
 | async announce(announce_text: str = None) -> Optional[str]
```
获取或设置群公告。（必须是群主，才能设置群公告）

<a name="wechaty.user.room.Room.qr_code"></a>
#### qr\_code

```python
 | async qr_code() -> str
```
获取群二维码。（可以用于扫码入群）

注：目前不支持该方法，待修复。

<a name="wechaty.user.room.Room.alias"></a>
#### alias

```python
 | async alias(member: Contact) -> Optional[str]
```
获取群成员在本群的昵称。

注：目前不支持该方法，待修复。

<a name="wechaty.user.room.Room.has"></a>
#### has

```python
 | async has(contact: Contact) -> bool
```
检查一个群中是否包含某个成员。

<a name="wechaty.user.room.Room.member_list"></a>
#### member\_list

```python
 | async member_list(query: Union[str, RoomMemberQueryFilter] = None) -> List[Contact]
```

通过关键字或 RoomMemberQueryFilter 对象查询满足条件的群成员列表。

<a name="wechaty.user.room.Room.member"></a>
#### member

```python
 | async member(query: Union[str, RoomMemberQueryFilter] = None) -> Optional[Contact]
```

通过关键字或 RoomMemberQueryFilter 对象查询满足条件的群成员。如果有多名满足条件的群成员，返回第一个。


<a name="wechaty.user.room.Room.owner"></a>
#### owner

```python
 | async owner() -> Optional[Contact]
```

查询群主。

<a name="wechaty.user.room.Room.avatar"></a>
#### avatar

```python
 | async avatar() -> FileBox
```

获取群头像图片。（微信无此功能）
