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
    * [.accept\(\)](friendship.md#Friendship+accept) ⇒ `Promise <void>`
    * [.hello\(\)](friendship.md#Friendship+hello) ⇒ `string`
    * [.contact\(\)](friendship.md#Friendship+contact) ⇒ `Contact`
    * [.type\(\)](friendship.md#Friendship+type) ⇒ `FriendshipType`
  * _静态方法_
    * [~~.send\(\)~~](friendship.md#Friendship.send)
    * [.add\(contact, hello\)](friendship.md#Friendship.add) ⇒ `Promise <void>`

### friendship.accept\(\) ⇒ `Promise <void>`

接受朋友请求

**类型**: [`Friendship`](friendship.md#Friendship)的实例方法  

#### 示例

```javascript
const bot = new Wechaty()
bot.on('friendship', async friendship => {
  try {
    console.log(`received friend event.`)
    switch (friendship.type()) {

    // 1. New Friend Request

    case bot.Friendship.Type.Receive:
      await friendship.accept()
      break

    // 2. Friend Ship Confirmed

    case bot.Friendship.Type.Confirm:
      console.log(`friend ship confirmed`)
      break
    }
  } catch (e) {
    console.error(e)
  }
})
.start()
```

### friendship.hello\(\) ⇒ `str`

Get verify message from

**类型**: [`Friendship`](friendship.md#Friendship)的实例方法  

**示例** 

_\(If request content is \`ding\`, then accept the friendship\)_

```javascript
const bot = new Wechaty()
bot.on('friendship', async friendship => {
  try {
    console.log(`received friend event from ${friendship.contact().name()}`)
    if (friendship.type() === bot.Friendship.Type.Receive && friendship.hello() === 'ding') {
      await friendship.accept()
    }
  } catch (e) {
    console.error(e)
  }
}
.start()
```

### friendship.contact\(\) ⇒ `Contact`

获取邀请的联系人对象

**类型**: [`Friendship`](friendship.md#Friendship)的实例方法  

#### 示例

```javascript
const bot = new Wechaty()
bot.on('friendship', friendship => {
  const contact = friendship.contact()
  const name = contact.name()
  console.log(`received friend event from ${name}`)
}
.start()
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

**类型** _\(If request content is \`ding\`, then accept the friendship\)_

```javascript
const bot = new Wechaty()
bot.on('friendship', async friendship => {
  try {
    if (friendship.type() === bot.Friendship.Type.Receive && friendship.hello() === 'ding') {
      await friendship.accept()
    }
  } catch (e) {
    console.error(e)
  }
}
.start()
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

```javascript
const memberList = await room.memberList()
for (let i = 0; i < memberList.length; i++) {
  await bot.Friendship.add(member, 'Nice to meet you! I am wechaty bot!')
}
```
