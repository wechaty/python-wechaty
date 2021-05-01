---
title: RoomInvitation
---

Accept room invitation

## RoomInvitation

accept room invitation

**Kind**: global class

* [RoomInvitation](room-invitation.md#RoomInvitation)
  * [.accept\(\)](room-invitation.md#RoomInvitation+accept) ⇒ `Promise <void>`
  * [.inviter\(\)](room-invitation.md#RoomInvitation+inviter) ⇒ `Promise <Contact>`
  * [.topic\(\)](room-invitation.md#RoomInvitation+topic) ⇒ `Promise <string>`
  * [~~.roomTopic\(\)~~](room-invitation.md#RoomInvitation+roomTopic) ⇒ `Promise <string>`
  * [.date\(\)](room-invitation.md#RoomInvitation+date) ⇒ `Promise <Date>`
  * [.age\(\)](room-invitation.md#RoomInvitation+age) ⇒ `Promise <number>`

### roomInvitation.accept\(\) ⇒ `Promise <void>`

Accept Room Invitation

**Kind**: instance method of [`RoomInvitation`](room-invitation.md#RoomInvitation)  

#### Example

```javascript
const bot = new Wechaty()
bot.on('room-invite', async roomInvitation => {
  try {
    console.log(`received room-invite event.`)
    await roomInvitation.accept()
  } catch (e) {
    console.error(e)
  }
}
.start()
```

### roomInvitation.inviter\(\) ⇒ `Promise <Contact>`

Get the inviter from room invitation

**Kind**: instance method of [`RoomInvitation`](room-invitation.md#RoomInvitation)  

#### Example

```javascript
const bot = new Wechaty()
bot.on('room-invite', async roomInvitation => {
  const inviter = await roomInvitation.inviter()
  const name = inviter.name()
  console.log(`received room invitation event from ${name}`)
}
.start()
```

### roomInvitation.topic\(\) ⇒ `Promise <string>`

Get the room topic from room invitation

**Kind**: instance method of [`RoomInvitation`](room-invitation.md#RoomInvitation)  

#### Example

```javascript
const bot = new Wechaty()
bot.on('room-invite', async roomInvitation => {
  const topic = await roomInvitation.topic()
  console.log(`received room invitation event from room ${topic}`)
}
.start()
```

### ~~roomInvitation.roomTopic\(\)~~

**Kind**: instance method of [`RoomInvitation`](room-invitation.md#RoomInvitation)  
**Deprecated:**: use topic\(\) instead

### roomInvitation.date\(\) ⇒ `Promise <Date>`

Get the invitation time

**Kind**: instance method of [`RoomInvitation`](room-invitation.md#RoomInvitation)

### roomInvitation.age\(\) ⇒ `Promise <number>`

Returns the roopm invitation age in seconds.

For example, the invitation is sent at time `8:43:01`, and when we received it in Wechaty, the time is `8:43:15`, then the age\(\) will return `8:43:15 - 8:43:01 = 14 (seconds)`

**Kind**: instance method of [`RoomInvitation`](room-invitation.md#RoomInvitation)
