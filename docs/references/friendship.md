---
title: Friendship
---

发送、接收好友请求和好友确认事件。

## Friendship

发送、接收好友请求和好友确认事件。

1. send request
2. receive request\(in friend event\)
3. confirmation friendship\(friend event\)

[Examples/Friend-Bot](https://github.com/wechaty/wechaty/blob/1523c5e02be46ebe2cc172a744b2fbe53351540e/examples/friend-bot.ts)

**Kind**: global class

* [Friendship](friendship.md#Friendship)
  * _instance_
    * [.accept\(\)](friendship.md#Friendship+accept) ⇒ `Promise <void>`
    * [.hello\(\)](friendship.md#Friendship+hello) ⇒ `string`
    * [.contact\(\)](friendship.md#Friendship+contact) ⇒ `Contact`
    * [.type\(\)](friendship.md#Friendship+type) ⇒ `FriendshipType`
  * _static_
    * [~~.send\(\)~~](friendship.md#Friendship.send)
    * [.add\(contact, hello\)](friendship.md#Friendship.add) ⇒ `Promise <void>`

### friendship.accept\(\) ⇒ `Promise <void>`

Accept Friend Request

**Kind**: instance method of [`Friendship`](friendship.md#Friendship)  

#### Example

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

### friendship.hello\(\) ⇒ `string`

Get verify message from

**Kind**: instance method of [`Friendship`](friendship.md#Friendship)  
**Example** _\(If request content is \`ding\`, then accept the friendship\)_

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

Get the contact from friendship

**Kind**: instance method of [`Friendship`](friendship.md#Friendship)  

#### Example

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

Return the Friendship Type

> Tips: FriendshipType is enum here. &lt;/br&gt;
>
> * FriendshipType.Unknown
> * FriendshipType.Confirm
> * FriendshipType.Receive
> * FriendshipType.Verify

**Kind**: instance method of [`Friendship`](friendship.md#Friendship)  
**Example** _\(If request content is \`ding\`, then accept the friendship\)_

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

_**Deprecated**_

use [Friendship\#add](friendship.md#friendship-add-contact-hello-promise) instead

**Kind**: static method of [`Friendship`](friendship.md#Friendship)

### Friendship.add\(contact, hello\) ⇒ `Promise <void>`

Send a Friend Request to a `contact` with message `hello`.

The best practice is to send friend request once per minute. Remeber not to do this too frequently, or your account may be blocked.

**Kind**: static method of [`Friendship`](friendship.md#Friendship)

| Param | Type | Description |
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
