---
title: ContactSelf
---

Bot itself will be encapsulated as a ContactSelf. This class is extends Contact.

## ContactSelf

Bot itself will be encapsulated as a ContactSelf.

> Tips: this class is extends Contact

**Kind**: global class

* [ContactSelf](contact-self.md#contactself)
  * [intance](contact-self.md#contactself)
    * [contactSelf.avatar\(\[file\]\) ⇒ `Promise <void | FileBox>`](contact-self.md#contactselfavatarfile-⇒-promise)
    * [contactSelf.qrcode\(\) ⇒ `Promise <string>`](contact-self.md#contactselfqrcode-⇒-promise)
    * [contactSelf.signature\(signature\) ⇒ `Promise <string>`](contact-self.md#contactselfsignaturesignature)
    * [contactSelf.name\(\[name\]\) ⇒ `Promise <void> | string`](contact-self.md#contactselfname-⇒-promisestring)

### contactSelf.avatar\(\[file\]\) ⇒ `Promise <void | FileBox>`

GET / SET bot avatar

**Kind**: instance method of [`ContactSelf`](contact-self.md#ContactSelf)

| Param | Type |
| :--- | :--- |
| \[file\] | `FileBox` |

**Example** _\( GET the avatar for bot, return {Promise&lt;FileBox&gt;}\)_

```javascript
// Save avatar to local file like `1-name.jpg`

bot.on('login', async user => {
  console.log(`user ${user} login`)
  const file = await user.avatar()
  const name = file.name
  await file.toFile(name, true)
  console.log(`Save bot avatar: ${user.name()} with avatar file: ${name}`)
})
```

**Example** _\(SET the avatar for a bot\)_

```javascript
import { FileBox }  from 'file-box'
bot.on('login', user => {
  console.log(`user ${user} login`)
  const fileBox = FileBox.fromUrl('https://wechaty.github.io/wechaty/images/bot-qr-code.png')
  await user.avatar(fileBox)
  console.log(`Change bot avatar successfully!`)
})
```

### contactSelf.qrcode\(\) ⇒ `Promise <string>`

Get bot qrcode

**Kind**: instance method of [`ContactSelf`](contact-self.md#ContactSelf)

#### Example

```javascript
import { generate } from 'qrcode-terminal'
bot.on('login', async user => {
  console.log(`user ${user} login`)
  const qrcode = await user.qrcode()
  console.log(`Following is the bot qrcode!`)
  generate(qrcode, { small: true })
})
```

### contactSelf.signature\(signature\) ⇒ `Promise <void>`

Change bot signature

**Kind**: instance method of [`ContactSelf`](contact-self.md#ContactSelf)

| Param | Description |
| :--- | :--- |
| signature | The new signature that the bot will change to |

#### Example

```javascript
bot.on('login', async user => {
  console.log(`user ${user} login`)
  try {
    await user.signature(`Signature changed by wechaty on ${new Date()}`)
  } catch (e) {
    console.error('change signature failed', e)
  }
})
```

### contactSelf.name\(\[name\]\) ⇒ `Promise<void> | string`

Get or change bot name.

**Kind**: instance method of [`ContactSelf`](contact-self.md#contactself)

| Param | Description |
| :--- | :--- |
| \[name\] | The new alias that the bot will change to |

#### Example

```javascript
bot.on('login', async user => {
  console.log(`user ${user} login`)
  const oldName = user.name() // get bot name
  try {
    await user.name(`${oldName}-${new Date().getTime()}`) // change bot name
  } catch (e) {
    console.error('change name failed', e)
  }
})
```
