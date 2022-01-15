
一个机器人就是`Wechaty`实例，所有用户相关模块都应该通过实例来获取，这样能保证服务连接的一致性，此外所有的逻辑应该以插件和事件订阅的形式组织，保证不同业务之间的隔离性以及业务内的内聚性。

## 一、支持的协议

一个Wechaty实例/派生类就是机器人对象，能够根据`TOKEN`找到连接的服务，获取用户自模块执行搜索，而这些信息都是由Wechaty实例管理。

> 由于服务的连接信息是保存到实例当中，故用户子模块一定要通过Wechaty实例来获取。例如：bot.Contact.find_all()

### 1.1 什么是协议

所有实现底层平台对接实现就是一个协议。

python-wechaty理论上能够对接所有IM平台，目前已经对接微信、微信公众号、钉钉、飞书以及WhatsApp等平台，源码都是基于TypeScript语言，可是通过`wechaty-puppet-service`能够将其服务以gRPC的形式暴露出来，提供给多语言`Wechaty`来连接。例如微信免费Web协议，底层实现是基于TyepScript编写，可是通过社区生态项目，可是都可以使用docker将接口的实现部署成服务。

比如[wechaty-puppet-wechat](https://github.com/wechaty/wechaty-puppet-wechat)能够通过[wechaty/wechaty:latest](https://hub.docker.com/r/wechaty/wechaty)镜像将其所有实现接口暴露成gRPC的服务，非常的方便，已然实现`write once, run anywhere`。

### 1.2 协议列表

目前python-wechaty能够使用wechaty生态中所有IM平台对接协议，协议列表如下所示：

* [wechaty-puppet-wechaty](https://github.com/wechaty/wechaty-puppet-wechat): 免费微信Web协议
* [wechaty-puppet-](https://github.com/wechaty/wechaty-puppet-macOS): 免费微信MacOs协议
* [wechaty-puppet-padlocal](https://github.com/wechaty/wechaty-puppet-padlocal): 付费微信Pad协议
* [wechaty-puppet-official-account](https://github.com/wechaty/wechaty-puppet-official-account): 微信公众号协议
* [wechaty-puppet-lark](https://github.com/wechaty/wechaty-puppet-lark): 飞书协议
* [wechaty-puppet-dingtalk](https://github.com/wechaty/wechaty-puppet-dingtalk): 钉钉协议
* [wechaty-puppet-teams](https://github.com/wechaty/wechaty-puppet-dingtalk): 微软Teams协议
* ......


## 二、Wechaty 模块详解

`Wechaty`类用来实例化机器人对象，控制机器人的整体逻辑，如：启动、注册监听事件、登录、注销等功能。


### 2.1 初始化

创建机器人实例：

| 参数 | 类型 | 默认值 |
| :--- | :--- | :--- |
| \[options\] | [`WechatyOptions`](wechaty.md#WechatyOptions) | `{}` |

**Example** _\(The World's Shortest ChatBot Code: 6 lines of JavaScript\)_

```javascript
const { Wechaty } = require('wechaty')
const bot = new Wechaty()
bot.on('scan',    (qrcode, status) => console.log(['https://api.qrserver.com/v1/create-qr-code/?data=',encodeURIComponent(qrcode),'&size=220x220&margin=20',].join('')))
bot.on('login',   user => console.log(`User ${user} logined`))
bot.on('message', message => console.log(`Message: ${message}`))
bot.start()
```

### wechaty.on\(event, listener\) ⇒ [`Wechaty`](wechaty.md#Wechaty)

当机器人获取到信息, 它会触发下面的事件

在这些事件函数中，您可以做任何您想做的事情。 主要事件名称如下：

* **scan**: 当机器人需要向您出示二维码来扫码登入的时候触发. 当您扫描二维码之后, 您便可以登入
* **login**: 当Bot成功登入时触发
* **logout**: 当机器人探测到账号登出时触发
* **message**: 当机器人收到新消息的时候触发

更多详见[WechatyEventName](wechaty.md#WechatyEventName)

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法
**返回值**: [`Wechaty`](wechaty.md#Wechaty) - - this for chaining, see advanced [chaining usage](https://github.com/wechaty/wechaty-getting-started/wiki/FAQ-EN#36-why-wechatyonevent-listener-return-wechaty)

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| event | [`WechatyEventName`](wechaty.md#WechatyEventName) | 触发wechaty事件(WechatyEvent) |
| listener | [`WechatyEventFunction`](wechaty.md#WechatyEventFunction) | WechatyEvent绑定的触发函数 |

**示例** _\(Event:scan\)_

```javascript
// Scan Event will emit when the bot needs to show you a QR Code for scanning

bot.on('scan', (url, code) => {
  console.log(`[${code}] Scan ${url} to login.` )
})
```

**示例** _\(Event:login \)_

```javascript
// Login Event will emit when bot login full successful.

bot.on('login', (user) => {
  console.log(`user ${user} login`)
})
```

**示例** _\(Event:logout \)_

```javascript
// Logout Event will emit when bot detected log out.

bot.on('logout', (user) => {
  console.log(`user ${user} logout`)
})
```

**示例** _\(Event:message \)_

```javascript
// Message Event will emit when there's a new message.

wechaty.on('message', (message) => {
  console.log(`message ${message} received`)
})
```

**示例** _\(Event:friendship \)_

```javascript
// Friendship Event will emit when got a new friend request, or friendship is confirmed.

bot.on('friendship', async (friendship) => {
  const contact = friendship.contact()
  if (friendship.type() === bot.Friendship.Type.Receive) { // 1. receive new friendship request from new contact
    let result = await friendship.accept()
    if (result) {
      console.log(`Request from ${contact.name()} is accept succesfully!`)
    } else {
      console.log(`Request from ${contact.name()} failed to accept!`)
    }
  } else if (friendship.type() === bot.Friendship.Type.Confirm) { // 2. confirm friendship
    console.log(`New friendship confirmed with ${contact.name()}`)
  }
})
```

**示例** _\(Event:room-join \)_

```javascript
// room-join Event will emit when someone join the room.

bot.on('room-join', async (room, inviteeList, inviter) => {
  const nameList = inviteeList.map(c => c.name()).join(',')
  console.log(`Room ${await room.topic()} got new member ${nameList}, invited by ${inviter}`)
})
```

**示例** _\(Event:room-leave \)_

```javascript
// room-leave Event will emit when someone leave the room.

bot.on('room-leave', async (room, leaverList, remover) => {
  const nameList = leaverList.map(c => c.name()).join(',')
  console.log(`Room ${await room.topic()} lost member ${nameList}, the remover is: ${remover}`)
})
```

**示例** _\(Event:room-topic \)_

```javascript
// room-topic Event will emit when someone change the room's topic.

bot.on('room-topic', async (room, topic, oldTopic, changer) => {
  console.log(`Room ${await room.topic()} topic changed from ${oldTopic} to ${topic} by ${changer.name()}`)
})
```

**示例** _\(Event:room-invite, RoomInvitation 已经封装为一个 RoomInvitation类. \)_

```javascript
// room-invite Event will emit when there's an room invitation.

bot.on('room-invite', async roomInvitation => {
  try {
    console.log(`received room-invite event.`)
    await roomInvitation.accept()
  } catch (e) {
    console.error(e)
  }
}
```

**示例** _\(Event:error \)_

```javascript
// error Event will emit when there's an error occurred.

bot.on('error', (error) => {
  console.error(error)
})
```

### wechaty.start\(\) ⇒ `None`

当您启动机器人时，机器人便开始尝试登录，您需要微信扫描二维码登录

> 提示: 所有的bot操作都需要在start\(\)完成之后才可以触发

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法

#### 示例

```python
from wechaty import Wechaty
import asyncio

async def main():
    bot = Wechaty()
    await bot.start()

asyncio.run(main())
```

### wechaty.stop\(\) ⇒ `None`

停止机器人

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法

#### 示例

```python
await bot.stop()
```

### wechaty.logout\(\) ⇒ `None`

让Bot登出微信

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法

#### 示例

```python
await bot.logout()
```

### wechaty.logonoff\(\) ⇒ `bool`

获取机器人的登入或者登出的状态, 返回一个布尔值

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法
**返回值**: 登入状态则返回True, 登出则返回False

#### Example

```javascript
if (bot.logonoff()) {
  console.log('Bot logined')
} else {
  console.log('Bot not logined')
}
```

### wechaty.userSelf\(\) ⇒ `ContactSelf`

获取当前用户

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法

#### 示例

```javascript
const contact = bot.userSelf()
console.log(`Bot is ${contact.name()}`)
```

### wechaty.say\(textOrContactOrFileOrUrl\) ⇒ `Promise <void>`

向 userSelf 发送消息，换句话说，bot 向自己发送消息。

> 注意: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| 文本, 联系人对象, 文件对象, 链接或者小程序对象 | `str` \| [`Contact`](contact.md#Contact) \| `FileBox` \| `UrlLink` \| `MiniProgram` | 发送文本、联系人名片、文件或链接到目标联系人。  您可以使用 [FileBox](https://github.com/wechaty/python-wechaty-puppet/tree/master/src/wechaty_puppet/file_box) 类来发送文件。 |

#### 示例

```javascript
const bot = new Wechaty()
await bot.start()
// after logged in

// 1. send text to bot itself
await bot.say('hello!')

// 2. send Contact to bot itself
const contact = bot.Contact.load('contactId')
await bot.say(contact)

// 3. send Image to bot itself from remote url
import { FileBox }  from 'file-box'
const fileBox = FileBox.fromUrl('https://wechaty.github.io/wechaty/images/bot-qr-code.png')
await bot.say(fileBox)

// 4. send Image to bot itself from local file
import { FileBox }  from 'file-box'
const fileBox = FileBox.fromFile('/tmp/text.jpg')
await bot.say(fileBox)

// 5. send Link to bot itself
const linkPayload = new UrlLink({
  description : 'WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
  thumbnailUrl: 'https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
  title       : 'Welcome to Wechaty',
  url         : 'https://github.com/wechaty/wechaty',
})
await bot.say(linkPayload)
```

### Wechaty.instance\(\[options\]\)

Get the global instance of Wechaty

**类型**: [`Wechaty`](wechaty.md#Wechaty)的实例方法

| 参数 | 类型 | 默认值 |
| :--- | :--- | :--- |
| \[options\] | [`WechatyOptions`](wechaty.md#WechatyOptions) | `{}` |

**示例** _\(世界上最短的Python ChatBot：9行代码\)_

```python
from wechaty import Wechaty

import asyncio
async def main():
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print('Scan QR Code to login: {}\nhttps://wechaty.js.org/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logged in'.format(user)))
    bot.on('message', lambda message: print('Message: {}'.format(message)))
    await bot.start()

asyncio.run(main())
```

## Puppet名称

The term [Puppet](https://github.com/wechaty/wechaty/wiki/Puppet) in Wechaty is an Abstract Class for implementing protocol plugins. The plugins are the component that helps Wechaty to control the Wechat\(that's the reason we call it puppet\). The plugins are named PuppetXXX, for example:

* [PuppetPuppeteer](https://github.com/wechaty/wechaty-puppet-puppeteer)
* [PuppetPadchat](https://github.com/lijiarui/wechaty-puppet-padchat)

**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| wechat4u | `string` | The default puppet, using the [wechat4u](https://github.com/nodeWechat/wechat4u) to control the [WeChat Web API](https://wx.qq.com/) via a chrome browser. |
| padchat | `string` | - Using the WebSocket protocol to connect with a Protocol Server for controlling the iPad Wechat program. |
| puppeteer | `string` | - Using the [google puppeteer](https://github.com/GoogleChrome/puppeteer) to control the [WeChat Web API](https://wx.qq.com/) via a chrome browser. |
| mock | `string` | - Using the mock data to mock wechat operation, just for test. |

## WechatyOptions

The option parameter to create a wechaty instance

**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| profile | `string` | Wechaty Name.            When you set this:            `new Wechaty({profile: 'wechatyName'})`            it will generate a file called `wechatyName.memory-card.json`.            This file stores the bot's login information.            If the file is valid, the bot can auto login so you don't need to scan the qrcode to login again.            Also, you can set the environment variable for `WECHATY_PROFILE` to set this value when you start.            eg:  `WECHATY_PROFILE="your-cute-bot-name" node bot.js`. This field is deprecated, please use `name` instead. [see more](https://github.com/wechaty/wechaty/issues/2049) |
| puppet | `PuppetModuleName` \| `Puppet` | Puppet name or instance |
| puppetOptions | `Partial.` | Puppet TOKEN |
| ioToken | `string` | Io TOKEN |

## WechatyEventName

Wechaty Class Event Type

**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| error | `string` | When the bot get error, there will be a Wechaty error event fired. |
| login | `string` | After the bot login full successful, the event login will be emitted, with a Contact of current logined user. |
| logout | `string` | Logout will be emitted when bot detected log out, with a Contact of the current login user. |
| heartbeat | `string` | Get bot's heartbeat. |
| friendship | `string` | When someone sends you a friend request, there will be a Wechaty friendship event fired. |
| message | `string` | Emit when there's a new message. |
| ready | `string` | Emit when all data has load completed, in wechaty-puppet-padchat, it means it has sync Contact and Room completed |
| room-join | `string` | Emit when anyone join any room. |
| room-topic | `string` | Get topic event, emitted when someone change room topic. |
| room-leave | `string` | Emit when anyone leave the room. |
| room-invite | `string` | Emit when there is a room invitation, see more in  [RoomInvitation](room-invitation.md)                                    If someone leaves the room by themselves, wechat will not notice other people in the room, so the bot will never get the "leave" event. |
| scan | `string` | A scan event will be emitted when the bot needs to show you a QR Code for scanning. &lt;/br&gt;                                    It is recommend to install qrcode-terminal\(run `npm install qrcode-terminal`\) in order to show qrcode in the terminal. |

## WechatyEventFunction

Wechaty Class Event Function

**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| error | `function` | \(this: Wechaty, error: Error\) =&gt; void callback function |
| login | `function` | \(this: Wechaty, user: ContactSelf\)=&gt; void |
| logout | `function` | \(this: Wechaty, user: ContactSelf\) =&gt; void |
| scan | `function` | \(this: Wechaty, url: string, code: number\) =&gt; void |
| heartbeat | `function` | \(this: Wechaty, data: any\) =&gt; void |
| friendship | `function` | \(this: Wechaty, friendship: Friendship\) =&gt; void |
| message | `function` | \(this: Wechaty, message: Message\) =&gt; void |
| ready | `function` | \(this: Wechaty\) =&gt; void |
| room-join | `function` | \(this: Wechaty, room: Room, inviteeList: Contact\[\],  inviter: Contact\) =&gt; void |
| room-topic | `function` | \(this: Wechaty, room: Room, newTopic: string, oldTopic: string, changer: Contact\) =&gt; void |
| room-leave | `function` | \(this: Wechaty, room: Room, leaverList: Contact\[\]\) =&gt; void |
| room-invite | `function` | \(this: Wechaty, room: Room, leaverList: Contact\[\]\) =&gt; void                                          see more in  [RoomInvitation](room-invitation.md) |
