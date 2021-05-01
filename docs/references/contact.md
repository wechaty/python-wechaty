---
title: Contact
---

All wechat contacts(friend) will be encapsulated as a Contact.

## Classes

[Contact](contact.md#Contact)

All wechat contacts\(friend\) will be encapsulated as a Contact. [Examples/Contact-Bot](https://github.com/wechaty/wechaty/blob/1523c5e02be46ebe2cc172a744b2fbe53351540e/examples/contact-bot.ts)

## Typedefs

[ContactQueryFilter](contact.md#ContactQueryFilter)

The way to search Contact

## Contact

All wechat contacts\(friend\) will be encapsulated as a Contact. [Examples/Contact-Bot](https://github.com/wechaty/wechaty/blob/1523c5e02be46ebe2cc172a744b2fbe53351540e/examples/contact-bot.ts)

**Kind**: global class **Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| id | `string` | Get Contact id. This function is depending on the Puppet Implementation, see [puppet-compatible-table](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table) |

* [Contact](contact.md#Contact)
  * _instance_
    * [.say\(textOrContactOrFileOrUrl\)](contact.md#Contact+say) ⇒ `Promise <void>`
    * [.name\(\)](contact.md#Contact+name) ⇒ `string`
    * [.alias\(newAlias\)](contact.md#Contact+alias) ⇒ `Promise <null | string | void>`
    * [.friend\(\)](contact.md#Contact+friend) ⇒ `boolean` \| `null`
    * [.type\(\)](contact.md#Contact+type) ⇒ `ContactType.Unknown` \| `ContactType.Personal` \| `ContactType.Official`
    * [.gender\(\)](contact.md#Contact+gender) ⇒ `ContactGender.Unknown` \| `ContactGender.Male` \| `ContactGender.Female`
    * [.province\(\)](contact.md#Contact+province) ⇒ `string` \| `null`
    * [.city\(\)](contact.md#Contact+city) ⇒ `string` \| `null`
    * [.avatar\(\)](contact.md#Contact+avatar) ⇒ `Promise <FileBox>`
    * [.sync\(\)](contact.md#Contact+sync) ⇒ `Promise <void>`
    * [.self\(\)](contact.md#Contact+self) ⇒ `boolean`
  * _static_
    * [.find\(query\)](contact.md#Contact.find) ⇒ `Promise <Contact | null>`
    * [.findAll\(\[queryArg\]\)](contact.md#Contact.findAll) ⇒ `Promise <Contact []>`

### contact.say\(textOrContactOrFileOrUrlLinkOrMiniProgram\) ⇒ `Promise <void>`

> Tips: This function is depending on the Puppet Implementation, see [puppet-compatible-table](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**Kind**: instance method of [`Contact`](contact.md#Contact)

| Param | Type | Description |
| :--- | :--- | :--- |
| textOrContactOrFileOrUrlLinkOrMiniProgram | `string` \| [`Contact`](contact.md#Contact) \| `FileBox` \| `UrlLink` \| `MiniProgram` | send text, Contact, file or UrlLink to contact.   You can use [FileBox](https://www.npmjs.com/package/file-box) to send file |

#### Example

```javascript
import { FileBox }  from 'file-box'
import {
  Wechaty,
  UrlLink,
  MiniProgram,
}  from 'wechaty'

const bot = new Wechaty()
await bot.start()
const contact = await bot.Contact.find({name: 'lijiarui'})  // change 'lijiarui' to any of your contact name in wechat

// 1. send text to contact

await contact.say('welcome to wechaty!')

// 2. send media file to contact

import { FileBox }  from 'file-box'
const fileBox1 = FileBox.fromUrl('https://wechaty.github.io/wechaty/images/bot-qr-code.png')
const fileBox2 = FileBox.fromFile('/tmp/text.txt')
await contact.say(fileBox1)
await contact.say(fileBox2)

// 3. send contact card to contact

const contactCard = bot.Contact.load('contactId')
await contact.say(contactCard)

// 4. send url link to contact

const urlLink = new UrlLink({
  description : 'WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
  thumbnailUrl: 'https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
  title       : 'Welcome to Wechaty',
  url         : 'https://github.com/wechaty/wechaty',
})
await contact.say(urlLink)

// 5. send MiniProgram (only supported by `wechaty-puppet-macpro`)

const miniProgram = new MiniProgram ({
  appid              : 'gh_0aa444a25adc',
  title              : '我正在使用Authing认证身份，你也来试试吧',
  pagePath           : 'routes/explore.html',
  description        : '身份管家',
  thumbUrl           : '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
  thumbKey           : '42f8609e62817ae45cf7d8fefb532e83',
});

await contact.say(miniProgram);
```

### contact.name\(\) ⇒ `string`

Get the name from a contact

**Kind**: instance method of [`Contact`](contact.md#Contact) **Example**

```javascript
const name = contact.name()
```

### contact.alias\(newAlias\) ⇒ `Promise <null | string | void>`

GET / SET / DELETE the alias for a contact

Tests show it will failed if set alias too frequently\(60 times in one minute\).

**Kind**: instance method of [`Contact`](contact.md#Contact)

| Param | Type |
| :--- | :--- |
| newAlias | `none` \| `string` \| `null` |

**Example** _\( GET the alias for a contact, return {\(Promise&lt;string \| null&gt;\)}\)_

```javascript
const alias = await contact.alias()
if (alias === null) {
  console.log('You have not yet set any alias for contact ' + contact.name())
} else {
  console.log('You have already set an alias for contact ' + contact.name() + ':' + alias)
}
```

**Example** _\(SET the alias for a contact\)_

```javascript
try {
  await contact.alias('lijiarui')
  console.log(`change ${contact.name()}'s alias successfully!`)
} catch (e) {
  console.log(`failed to change ${contact.name()} alias!`)
}
```

**Example** _\(DELETE the alias for a contact\)_

```javascript
try {
  const oldAlias = await contact.alias(null)
  console.log(`delete ${contact.name()}'s alias successfully!`)
  console.log(`old alias is ${oldAlias}`)
} catch (e) {
  console.log(`failed to delete ${contact.name()}'s alias!`)
}
```

### contact.friend\(\) ⇒ `boolean` \| `null`

Check if contact is friend

> Tips: This function is depending on the Puppet Implementation, see [puppet-compatible-table](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**Kind**: instance method of [`Contact`](contact.md#Contact) **Returns**: `boolean` \| `null` - True for friend of the bot False for not friend of the bot, null for unknown. **Example**

```javascript
const isFriend = contact.friend()
```

### contact.type\(\) ⇒ `ContactType.Unknown` \| `ContactType.Personal` \| `ContactType.Official`

Return the type of the Contact

> Tips: ContactType is enum here.

**Kind**: instance method of [`Contact`](contact.md#Contact) **Example**

```javascript
const bot = new Wechaty()
await bot.start()
const isOfficial = contact.type() === bot.Contact.Type.Official
```

### contact.gender\(\) ⇒ `ContactGender.Unknown` \| `ContactGender.Male` \| `ContactGender.Female`

Contact gender

> Tips: ContactGender is enum here.

**Kind**: instance method of [`Contact`](contact.md#Contact) **Example**

```javascript
const gender = contact.gender() === bot.Contact.Gender.Male
```

### contact.province\(\) ⇒ `string` \| `null`

Get the region 'province' from a contact

**Kind**: instance method of [`Contact`](contact.md#Contact) **Example**

```javascript
const province = contact.province()
```

### contact.city\(\) ⇒ `string` \| `null`

Get the region 'city' from a contact

**Kind**: instance method of [`Contact`](contact.md#Contact) **Example**

```javascript
const city = contact.city()
```

### contact.avatar\(\) ⇒ `Promise <FileBox>`

Get avatar picture file stream

**Kind**: instance method of [`Contact`](contact.md#Contact) **Example**

```javascript
// Save avatar to local file like `1-name.jpg`

const file = await contact.avatar()
const name = file.name
await file.toFile(name, true)
console.log(`Contact: ${contact.name()} with avatar file: ${name}`)
```

### contact.sync\(\) ⇒ `Promise <void>`

Force reload data for Contact, Sync data from lowlevel API again.

**Kind**: instance method of [`Contact`](contact.md#Contact) **Example**

```javascript
await contact.sync()
```

### contact.self\(\) ⇒ `boolean`

Check if contact is self

**Kind**: instance method of [`Contact`](contact.md#Contact) **Returns**: `boolean` - True for contact is self, False for contact is others **Example**

```javascript
const isSelf = contact.self()
```

### Contact.find\(query\) ⇒ `Promise <Contact | null>`

Try to find a contact by filter: {name: string \| RegExp} / {alias: string \| RegExp}

Find contact by name or alias, if the result more than one, return the first one.

**Kind**: static method of [`Contact`](contact.md#Contact) **Returns**: `Promise.` - If can find the contact, return Contact, or return null

| Param | Type |
| :--- | :--- |
| query | [`ContactQueryFilter`](contact.md#ContactQueryFilter) |

#### Example

```javascript
const bot = new Wechaty()
await bot.start()
const contactFindByName = await bot.Contact.find({ name:"ruirui"} )
const contactFindByAlias = await bot.Contact.find({ alias:"lijiarui"} )
```

### Contact.findAll\(\[queryArg\]\) ⇒ `Promise <Contact []>`

Find contact by `name` or `alias`

If use Contact.findAll\(\) get the contact list of the bot. Include the contacts from bot's rooms.

#### definition

* `name`   the name-string set by user-self, should be called name
* `alias`  the name-string set by bot for others, should be called alias

**Kind**: static method of [`Contact`](contact.md#Contact)

| Param | Type |
| :--- | :--- |
| queryArg | [`ContactQueryFilter`](contact.md#ContactQueryFilter) |

#### Example

```javascript
const bot = new Wechaty()
await bot.start()
const contactList = await bot.Contact.findAll()                      // get the contact list of the bot
const contactList = await bot.Contact.findAll({ name: 'ruirui' })    // find all of the contacts whose name is 'ruirui'
const contactList = await bot.Contact.findAll({ alias: 'lijiarui' }) // find all of the contacts whose alias is 'lijiarui'
```

## ContactQueryFilter

The way to search Contact

**Kind**: global typedef **Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| name | `string` | The name-string set by user-self, should be called name |
| alias | `string` | The name-string set by bot for others, should be called alias [More Detail](https://github.com/wechaty/wechaty/issues/365) |
