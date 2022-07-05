---
title: Message
---
<!-- ::: wechaty.user.message.Message.talker
    handlers: python
    selection:
      members: 
        - __init__
        - to
        - talker
    rendering:
      show_root_heading: yes
      show_root_full_path: false
      members_order: source
      heading_level: 1 -->


<!-- 消息处理对象。 -->

## ::: wechaty.user.message.Message

<!-- 接受和发送的消息都封装成`Message`对象。 -->

<!-- [示例/Ding-Dong-Bot](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/ding-dong-bot.py)

**类型**: 全局对象

* [Message](message.md#Message)
  * _实例方法_
    * [~~.from\(\)~~](message.md#Message+from) ⇒ `Contact`
    * [.talker\(\)](message.md#Message+talker) ⇒ `Contact`
    * [.to\(\)](message.md#Message+to) ⇒ `Optional[Contact]`
    * [.room\(\)](message.md#Message+room) ⇒ `Optional[Room]`
    * [.text\(\)](message.md#Message+text) ⇒ `str`
    * [.say\(textOrContactOrFile\)](message.md#Message+say) ⇒ `None`
    * [.type\(\)](message.md#Message+type) ⇒ `MessageType`
    * [.is_self\(\)](message.md#Message+isSelf) ⇒ `bool`
    * [~~.mention\(\)~~](message.md#Message+mention) ⇒ `List[Contact]`
    * [.mention_self\(\)](message.md#Message+mentionSelf) ⇒ `bool`
    * [.mention_text\(\)](message.md#Message+mentionText) ⇒ `str`
    * [.mention_list\(\)](message.md#Message+mentionList) ⇒ `List[Contact]`
    * [.forward\(to\)](message.md#Message+forward) ⇒ `None`
    * [.date\(\)](message.md#Message+date) ⇒ `datetime`
    * [.age\(\)](message.md#Message+age) ⇒ `int`
    * [.to_file_box\(\)](message.md#Message+toFileBox) ⇒ `FileBox`
    * [.to_image\(\)](message.md#Message+toImage) ⇒ `Image`
    * [.to_contact\(\)](message.md#Message+toContact) ⇒ `Contact`
    * [.to_url_link\(\)](message.md#Message+toUrlLink) ⇒ `UrlLink`
    * [.to_url_linkto_mini_program\(\)](message.md#Message+toMiniProgram) ⇒ `UrlLink`
    * [.say\(textOrContactOrFileOrUrl, mention_ids\)](contact.md#Message+say) ⇒ `Optional[Message]`
    * [.to_recalled\(\)](contact.md#Message+toRecalled) ⇒ `Message`
    * [.recall\(\)](contact.md#Message+recall) ⇒ `bool`
  * _静态方法_
    * [.find\(\)](message.md#Message.find) ⇒ `Optional[Message]`
    * [.find_all\(\)](message.md#Message.findAll) ⇒ `List[Message]` -->
    

<!-- ### ~~def from\(self\)~~ ⇒ `Contact`

已弃用, 详见[message.talker\(\)](message.md#Message+talker) -->

<!-- ### def talker\(self\) ⇒ `Contact`

获取消息的发送者。

**类型**: [`Message`](message.md#Message)的实例方法 

**示例**

```python
import asyncio
from wechaty import Wechaty, Message

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        print(msg.talker())

asyncio.run(MyBot().start())
```

### def to\(self\) ⇒ `Optional[Contact]`

获取消息的接收者, 如果消息是在群聊发出的`Message.to()`会返回None, 请使用 `Message.room()` 获取群聊对象.

**类型**: [`Message`](message.md#Message)的实例方法 

#### 示例

```python
import asyncio
from wechaty import Wechaty, Message, Contact

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        talker: Contact = msg.talker()
        text: str = msg.text()
        to_contact = msg.to()
        if to_contact:
            name = to_contact.name
            print(f"接收者: {name} 联系人: {talker.name} 内容: {text}")
        else:
            print(f"联系人: {talker.name} 内容: {text}")


asyncio.run(MyBot().start())
``` -->
<!-- ### def room\(self\) ⇒ `Optional[Room]`

获取消息来自的群聊. 如果消息不是来自群聊, 则返回None

**类型**: [`Message`](message.md#Message)的实例方法

#### 示例

```python
import asyncio
from wechaty import Wechaty, Message, Contact

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        talker: Contact = msg.talker()
        text: str = msg.text()
        room = msg.room()
        if room:
            room_name = await room.topic()
            print(f"群聊名: {room_name} 联系人(消息发送者): {talker.name} 内容: {text}")
        else:
            print(f"联系人: {talker.name} 内容: {text}")


asyncio.run(MyBot().start())
```

### ~~def content\(\)~~

_**已弃用**_

请使用[text](message.md#Message+text)

**类型**: [`Message`](message.md#Message)的实例方法 

### def text\(self\) ⇒ `str`

获取对话的消息文本

**类型**: [`Message`](message.md#Message)的实例方法  

**示例**

```python
import asyncio
from wechaty import Wechaty, Message, Contact

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        talker: Contact = msg.talker()
        text: str = msg.text()
        room = msg.room()
        if room:
            room_name = await room.topic()
            print(f"群聊名: {room_name} 联系人(消息发送者): {talker.name} 内容: {text}")
        else:
            print(f"联系人: {talker.name} 内容: {text}")


asyncio.run(MyBot().start())
```

### async def recall\(self\) ⇒ `bool`

撤回这条信息

**类型**: [`Message`](message.md#Message)的实例方法

**返回值**: 返回撤回消息是否成功, 成功为`True`, 失败则为`False`


### async def to_recalled\(self\) ⇒ `Message`

获取撤回的信息的文本

**类型**: [`Message`](message.md#Message)的实例方法   

**示例**

```python
import asyncio
from wechaty import Wechaty, Message
from wechaty_puppet import MessageType

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        if msg.type() == MessageType.MESSAGE_TYPE_RECALLED:
            recalled_message = await msg.to_recalled()
            print(f"{recalled_message}被撤回")

asyncio.run(MyBot().start())
```

### async def say(self, msg: `Union[str, Contact, FileBox, UrlLink, MiniProgram]`, mention_ids: `Optional[List[str]]` = None)  ⇒ `Optional[Message]`

向联系人或群聊发送一段文字, 名片, 媒体文件或者链接

> 注意: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Message`](message.md#Message)的实例方法 

**参阅**: [Examples/ding-dong-bot](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/ding-dong-bot.py)

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| textOrContactOrFileOrUrlLinkOrMiniProgram | `string` \| `Contact` \| `FileBox` \| `UrlLink` \| `MiniProgram` | 发送 `文本`, `媒体文件` 或者 `链接`. 您可以使用 [FileBox](https://github.com/wechaty/python-wechaty-puppet/tree/master/src/wechaty_puppet/file_box) 类来发送文件。 |

#### 示例

```python
import asyncio
from wechaty import Wechaty, Message
from wechaty import Wechaty, Contact, FileBox, UrlLink


class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        text = msg.text()

        # 1. 发送文字到联系人
        if text == "叮":
            await msg.say('咚')
            return

        # 2. 发送媒体文件到联系人
        if text == "媒体":
            file_box1 = FileBox.from_url('https://wechaty.github.io/wechaty/images/bot-qr-code.png', "bot-qr-code.png")
            file_box2 = FileBox.from_file('text.txt', "text.txt")
            await msg.say(file_box1)
            await msg.say(file_box2)
            return

        # 3. 发送名片到联系人
        if text == "名片":
            contact_card = self.Contact.load('lijiarui')  # 把`lijiarui`更改为您在微信中的任意联系人的姓名
            await msg.say(contact_card)
            return

        # 4. 发送链接到联系人
        if text == "链接":
            url_link = UrlLink.create(
                description='WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
                thumbnail_url='https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
                title='Welcome to Wechaty',
                url='https://github.com/wechaty/wechaty',
            )
            await msg.say(url_link)
            return

        # 5. 发送小程序 (暂时只有`wechaty-puppet-macpro`支持该服务)

        if text == "小程序":
            miniProgram = self.MiniProgram.create_from_json({
                "appid": 'gh_0aa444a25adc',
                "title": '我正在使用Authing认证身份，你也来试试吧',
                "pagePath": 'routes/explore.html',
                "description": '身份管家',
                "thumbUrl": '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
                "thumbKey": '42f8609e62817ae45cf7d8fefb532e83',
            })
            await msg.say(miniProgram)
            return

asyncio.run(MyBot().start())
```

### def type\(self\) ⇒ `MessageType`

获取消息的类型

> 注意: `MessageType`是枚举类型; <br/>
>     `from wechaty_puppet import MessageType`
>*    MessageType.MESSAGE_TYPE_UNSPECIFIED
>*    MessageType.MESSAGE_TYPE_ATTACHMENT
>*    MessageType.MESSAGE_TYPE_AUDIO
>*    MessageType.MESSAGE_TYPE_CONTACT
>*    MessageType.MESSAGE_TYPE_EMOTICON
>*    MessageType.MESSAGE_TYPE_IMAGE
>*    MessageType.MESSAGE_TYPE_TEXT
>*    MessageType.MESSAGE_TYPE_VIDEO
>*    MessageType.MESSAGE_TYPE_CHAT_HISTORY
>*    MessageType.MESSAGE_TYPE_LOCATION
>*    MessageType.MESSAGE_TYPE_MINI_PROGRAM 
>*    MessageType.MESSAGE_TYPE_TRANSFER 
>*    MessageType.MESSAGE_TYPE_RED_ENVELOPE 
>*    MessageType.MESSAGE_TYPE_RECALLED 
>*    MessageType.MESSAGE_TYPE_URL 

**类型**: [`Message`](message.md#Message)的实例方法 

**示例**

```python
import asyncio
from wechaty import Wechaty, Message
from wechaty_puppet import MessageType

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        if msg.type() == MessageType.MESSAGE_TYPE_TEXT:
            print(f"这是个文本消息")

asyncio.run(MyBot().start())

```

### def is_self\(self\) ⇒ `bool`

检查这个消息是否是由自己发出的

**类型**: [`Message`](message.md#Message)的实例方法  

**返回值**: `bool` - - 返回 `True` 如果是Bot发出的消息, 如果是他人发出的则返回`False`. 

**示例**

```python
import asyncio
from wechaty import Wechaty, Message
from wechaty_puppet import MessageType

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        if msg.is_self():
            print("这个是Bot自己发出的消息")
        else:
            print("这是由别人发出的消息")

asyncio.run(MyBot().start())
```

### ~~def mention\(\)~~ ⇒ `List[Contact]`

已弃用, 请使用[.mention_list\(\)](message.md#Message+mentionList)

### async def mention_list\(self\) ⇒ `List[Contact]`

以列表的形式获取消息所提及\(@\)的人.

消息事件表如下

|  | Web\(网页版\) | Mac PC Client\(苹果电脑端\) | iOS Mobile\(IOS系统移动端\) | android Mobile\(安卓移动端\) |
| :--- | :---: | :---: | :---: | :---: |
| \[You were mentioned\] tip \(\[有人@我\]的提示\) | ✘ | √ | √ | √ |
| Identify magic code \(8197\) by copy & paste in mobile | ✘ | √ | √ | ✘ |
| Identify magic code \(8197\) by programming | ✘ | ✘ | ✘ | ✘ |
| Identify two contacts with the same roomAlias by \[You were  mentioned\] tip | ✘ | ✘ | √ | √ |

以下是表格的中文粗译

|  | Web\(网页版\) | Mac PC Client\(苹果电脑端\) | iOS Mobile\(IOS系统移动端\) | android Mobile\(安卓移动端\) |
| :--- | :---: | :---: | :---: | :---: |
| \[有人@我\]的提示 | ✘ | √ | √ | √ |
| 区分移动端复制粘贴的魔法代码 `0d8197 \u0x2005` | ✘ | √ | √ | ✘ |
| 通过编程区分魔法代码`0d8197 \u0x2005`| ✘ | ✘ | ✘ | ✘ |
| 区分两个拥有相同群聊昵称的人的\[有人@我\]的提示  | ✘ | ✘ | √ | √ |

注: `\u0x2005` 为不可见字符, 提及\(@\)的消息的格式一般为 `@Gary\u0x2005`

**类型**: [`Message`](message.md#Message)的实例方法  

**返回值**: `List[Contact]` - - 以列表的形式获取消息所提及\(@\)的人.

**示例**

```python
import asyncio
from wechaty import Wechaty,  Message

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact_mention_list = await msg.mention_list()
        print(contact_mention_list)

asyncio.run(MyBot().start())
```

### async def mention_self\(self\) ⇒ `bool`

**类型**: [`Message`](message.md#Message)的实例方法  

**返回值**: `bool` - - 如果这个消息提及(@)了Bot, 则返回True 

**示例**

```python
import asyncio
from wechaty import Wechaty, Message

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        print(await msg.mention_self())

asyncio.run(MyBot().start())
```

### async def mention_text\(self\)⇒ `str`

返回过滤掉`@name`后的消息 

**类型**: [`Message`](message.md#Message)的实例方法  

**返回值**: `str` - - 返回过滤掉`@name`后的消息 

**示例**

```python
import asyncio
from wechaty import Wechaty, Message

class MyBot(Wechaty):
    # 原消息为 `@Gary Helloworld`
    async def on_message(self, msg: Message) -> None:
        print(await msg.mention_text()) # 打印`Helloworld`

asyncio.run(MyBot().start())
```

### async def forward\(self, to: `Union[Room, Contact]`\) ⇒ `None`

转发接收到的信息. 此操作不会触发on-message事件.

**类型**: [`Message`](message.md#Message)的实例方法  

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| to | `Union[Room, Contact]` \| 群聊或者联系人, 消息的收件人、群聊房间或联系人 |

#### 示例

```python
import asyncio
from wechaty import Wechaty,  Message

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room = await self.Room.find("wechaty")
        if room:
            await msg.forward(room)
            print("成功转发消息到wechaty群聊")
            
asyncio.run(MyBot().start())
```

### def date\(self\) ⇒ `datetime`

获取消息发送的时间

**类型**: [`Message`](message.md#Message)的实例方法 

### def age\(self\) ⇒ `int`

获取当前距离已接收到的这条消息的时间的间隔

举个例子, 有条消息是`8:43:01`发送的, 而当我们在Wechaty中接收到它的时候时间已经为 `8:43:15`, 那么这时 `age()`返回的值为 `8:43:15 - 8:43:01 = 14 (秒)`

**类型**: [`Message`](message.md#Message)的实例方法 

### ~~def file\(\)~~

_**已弃用**_

请使用 [to_file_box](message.md#Message+toFileBox)

**类型**: [`Message`](message.md#Message)的实例方法 

### async def to_file_box\(self\) ⇒ `FileBox`

从消息中提取媒体文件，并将其封装为FileBox类返回。

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Message`](message.md#Message)的实例方法 

 .to_image

### async def to_mini_program\(self\) ⇒ `MiniProgram`

从消息中提取小程序卡片，并将其封装为MiniProgramM类返回。

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Message`](message.md#Message)的实例方法 


### def to_image\(self\) ⇒ `Image`

从消息中提取图像文件，以便我们可以使用不同的图像大小。

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Message`](message.md#Message)的实例方法 


### async def to_contact\(self\) ⇒ `Contact`

获取消息中的联系人卡片, 并从卡片中提取联系人将其封装到联系人类中返回

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Message`](message.md#Message)的实例方法 

### async def to_url_link\(self\) ⇒ `UrlLink`

获取消息的UrlLink, 从消息中提取UrlLink，并封装到UrlLink类中返回

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Message`](message.md#Message)的实例方法 

### `@classmethod` async def find(cls, talker_id: `Optional[str]` = None, message_id: `Optional[str]` = None, room_id: `Optional[str]` = None, text: `Optional[str]` = None, to_id: `Optional[str]` = None, message_type: `Optional[MessageType]` = None) ⇒ `Optional[Message]`

在缓存中查找消息

**Kind**:  [`Message`](message.md#Message)的静态方法

### `@classmethod` async def find_all(cls, talker_id: `Optional[str]` = None, message_id: `Optional[str]` = None, room_id: `Optional[str]` = None, text: `Optional[str]` = None, to_id: `Optional[str]` = None, message_type: `Optional[MessageType]` = None) ⇒ `List[Message]`

在缓存中查找消息

**类型**: [`Message`](message.md#Message)的静态方法 -->
