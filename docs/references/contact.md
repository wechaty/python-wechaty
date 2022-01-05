---
title: Contact
---

## Classes

所有的微信联系人（朋友）都会被封装成一个`Contact`联系人对象。


## Contact

所有的微信联系人（朋友）都会被封装成一个`Contact`联系人对象。示例: 
[Examples/Contact-Bot](https://github.com/wechaty/wechaty/blob/1523c5e02be46ebe2cc172a744b2fbe53351540e/examples/contact-bot.ts)

**类型**: 全局**属性**

| **属性名** | 类型 | **描述** |
| :--- | :--- | :--- |
| id | `string` | 获取联系人对象的id. 此函数取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table) |

* [Contact](contact.md#Contact)
  * _实例方法_
    * [.say\(textOrContactOrFileOrUrl\)](contact.md#Contact+say) ⇒ `Message`
    * [.name](contact.md#Contact+name)⇒ `str`
    * [.alias\(new\_alias\)](contact.md#Contact+alias) ⇒ `None | str | None`
    * [.friend\(\)](contact.md#Contact+friend) ⇒ `bool` \| `None`
    * [.type\(\)](contact.md#Contact+type) ⇒ `ContactType.CONTACT_TYPE_UNSPECIFIED` \| `ContactType.CONTACT_TYPE_PERSONAL` \| `ContactType.CONTACT_TYPE_OFFICIAL` \| `CONTACT_TYPE_CORPORATION`
    * [.gender\(\)](contact.md#Contact+gender) ⇒ `ContactGender.CONTACT_GENDER_UNSPECIFIED` \| `ContactGender.CONTACT_GENDER_MALE` \| `ContactGender.CONTACT_GENDER_FEMALE`
    * [.province\(\)](contact.md#Contact+province) ⇒ `str` \| `None`
    * [.city\(\)](contact.md#Contact+city) ⇒ `str` \| `None`
    * [.avatar\(\)](contact.md#Contact+avatar) ⇒ `FileBox`
    * [.sync\(\)](contact.md#Contact+sync) ⇒ `None`
    * [.self\(\)](contact.md#Contact+self) ⇒ `bool`
  * _静态方法_
    * [.find\(query\)](contact.md#Contact.find) ⇒ `Contact | None`
    * [.findAll\(\[queryArg\]\)](contact.md#Contact.findAll) ⇒ `List[Contact]`

### contact.say\(textOrContactOrFileOrUrlLinkOrMiniProgram\) ⇒ `None`

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Contact`](contact.md#Contact)的实例方法

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| 文本, 联系人对象, 文件对象, 链接或者小程序对象 | `str` \| [`Contact`](contact.md#Contact) \| `FileBox` \| `UrlLink` \| `MiniProgram` | 发送文本、联系人名片、文件或链接到目标联系人。  您可以使用 [FileBox](https://www.npmjs.com/package/file-box) 类来发送文件。 |

#### 示例

```python
import asyncio
from wechaty import Wechaty
from wechaty import FileBox, UrlLink
from wechaty_puppet import ContactQueryFilter


class MyBot(Wechaty):

    async def on_login(self, payload) -> None:
        contact = await self.Contact.find(
            ContactQueryFilter(name="lijiarui"))  # 把`lijiarui`更改为您在微信中的任意联系人的姓名

        # 1. 发送文字到联系人
        await contact.say('welcome to wechaty!')

        # 2. 发送媒体文件到联系人
        fileBox1 = FileBox.from_url('https://wechaty.github.io/wechaty/images/bot-qr-code.png', "bot-qr-code.png")
        fileBox2 = FileBox.from_file('text.txt', "text.txt")
        await contact.say(fileBox1)
        await contact.say(fileBox2)

        # 3. 发送名片到联系人
        contactCard = self.Contact.load('lijiarui')  # 把`lijiarui`更改为您在微信中的任意联系人的姓名
        await contact.say(contactCard)

        # 4. 发送链接到联系人

        urlLink = UrlLink.create(
            description='WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
            thumbnail_url='https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
            title='Welcome to Wechaty',
            url='https://github.com/wechaty/wechaty',
        )
        await contact.say(urlLink)

        # 5. 发送小程序 (暂时只有`wechaty-puppet-macpro`支持该服务)

        miniProgram = self.MiniProgram.create_from_json({
            "appid": 'gh_0aa444a25adc',
            "title": '我正在使用Authing认证身份，你也来试试吧',
            "pagePath": 'routes/explore.html',
            "description": '身份管家',
            "thumbUrl": '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
            "thumbKey": '42f8609e62817ae45cf7d8fefb532e83',
        })

        await contact.say(miniProgram)

asyncio.run(MyBot().start())
```

### contact.name ⇒ `str`

获取联系人对象的名字

**类型**:  [`Contact`](contact.md#Contact) 的实例方法

**示例:**

```python
name: str = contact.name
```

### contact.alias\(newAlias\) ⇒ `None | str | None`

为一个联系人获取 / 设置 / 删除别名

>  测试表明如果过于频繁地设置别名会导致失败\(每分钟60次\).

**类型**:  [`Contact`](contact.md#Contact)对象的实例方法

**返回值**: Promise&lt;string \| null&gt;

| 参数 | 类型 |
| :--- | :--- |
| newAlias | `None` \| `str` \| `None` |



**示例:**
_\(**获取**联系人对象的别名\(备注\)_

```python
alias = await contact.alias()
if alias is None or alias == "":
    print('您还没有为联系人设置任何别名' + contact.name)
else:
    print('您已经为联系人设置了别名 ' + contact.name + ':' + alias)
```

**示例**

_\(为一个联系人**设置**别名\(备注\)\)_

```python
try:
    await contact.alias('lijiarui')
    print(f"改变{contact.name}的备注成功!")
except Exception:
    print(f"改变{contact.name}的备注失败~")
```

**示例** 

_\(**删除**给联系人设置的别名\(备注\)\)_

```python
try:
    oldAlias = await contact.alias(None)
    print(f"成功删除{contact.name}的备注!")
    print(f"旧的备注名为{oldAlias}")
except Exception:
    print(f"删除{contact.name}的备注失败!")
```

### contact.friend\(\) ⇒ `bool` \| `None`

检查这个联系人对象是否是自己的朋友

> 注意: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Contact`](contact.md#Contact) 的实例方法

**返回值**: `bool` \| `None` - 如果是自己的朋友则返回True, 不是则返回False, Unknown(未知)则返回None.

**示例**

```python
isFriend = contact.is_friend()
print(isFriend)
```

### contact.type\(\) ⇒ `ContactType.CONTACT_TYPE_UNSPECIFIED` \| `ContactType.CONTACT_TYPE_PERSONAL` \| `ContactType.CONTACT_TYPE_OFFICIAL` \| `CONTACT_TYPE_CORPORATION`

返回联系人的类型

> 注意: ContactType是个枚举类型.

**类型**: [`Contact`](contact.md#Contact)的实例方法 

**示例**

```python
import asyncio
from wechaty import Wechaty, Message, ContactType

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact = msg.talker()
        print(contact.type() == ContactType.CONTACT_TYPE_OFFICIAL)

asyncio.run(MyBot().start())
```

### contact.gender\(\) ⇒ `ContactGender.CONTACT_GENDER_UNSPECIFIED` \| `ContactGender.CONTACT_GENDER_MALE` \| `ContactGender.CONTACT_GENDER_FEMALE`

获取联系人的性别

> 注意: ContactGender是个枚举类型.

**类型**: [`Contact`](contact.md#Contact)的实例方法 

**示例**

```python
import asyncio
from wechaty import Wechaty, Message, ContactGender


class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact = msg.talker()
        # 联系人是否为男性?
        print(contact.gender() == ContactGender.CONTACT_GENDER_MALE)

asyncio.run(MyBot().start())
```

### contact.province\(\) ⇒ `str` \| `None`

获取一个联系人-的省份信息

**类型**: [`Contact`](contact.md#Contact)的实例方法 

**示例**

```python
province: str = contact.province()
```

### contact.city\(\) ⇒ `str` \| `None`

获取联系人所设置的城市

**类型**: [`Contact`](contact.md#Contact)的实例方法 

**示例**

```python
city: str = contact.city()
```

### contact.avatar\(\) ⇒ `FileBox`

获取联系人头像图片的文件流

**类型**: [`Contact`](contact.md#Contact)的实例方法 

**示例**

```python
# 以类似 `1-name.jpg`的格式保存头像图片到本地
import asyncio
from wechaty import Wechaty, Message, FileBox

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact = msg.talker()
        avatar: "FileBox" = await contact.avatar()
        name = avatar.name
        await avatar.to_file(name, True)
        print(f"联系人: {contact.name} 和头像: {name}")

asyncio.run(MyBot().start())
```

### contact.sync\(\) ⇒ `None`

强制重新加载联系人的数据，再次从低级 API 同步数据。

**类型**: [`Contact`](contact.md#Contact)的实例方法 

**示例**

```python
await contact.sync()
```

### contact.self\(\) ⇒ `bool`

检查该联系人对象是不是Bot自身

**类型**: [`Contact`](contact.md#Contact)的实例方法

**返回值**: `bool` - 如果该联系人对象是Bot自身则返回True, 若不是则返回False 

**示例**

```python
isSelf: bool = contact.self()
```

### Contact.find\(query\) ⇒ `Contact | None`

尝试通过过滤器查找联系人: {name: string \| RegExp} / {alias: string \| RegExp}

通过联系人的名字(name)或者别名(alias)来获取联系人对象, 如果查找的结果大于一个, 则返回第一个.

**类型**: [`Contact`](contact.md#Contact)的静态方法 

**返回值**: `Promise.` - 如果能找到联系人，则返回找到的联系人对象，否则返回`None`

| 参数 | 类型 |
| :--- | :--- |
| query | [`ContactQueryFilter`](contact.md#ContactQueryFilter) |

#### 示例

```python
import asyncio
from wechaty import Wechaty
from wechaty_puppet import ContactQueryFilter

class MyBot(Wechaty):

    async def on_login(self, payload) -> None:
        contact = await self.Contact.find(ContactQueryFilter(name="lijiarui"))
        contact = await self.Contact.find(ContactQueryFilter(alias="ruirui"))
        
asyncio.run(MyBot().start())
```

### Contact.findAll\(\[queryArg\]\) ⇒ `List[Contact]`

通过 `name` 或者 `alias` 查找并获取联系人对象

使用 Contact.findAll\(\) 获取机器人的联系人列表。 包括来自机器人加入的房间内的联系人。

#### 定义

* `name`   由用户自己设置的名字, 叫做name
* `alias`  由Bot为联系人设置的名字\(备注/别名\). 该值可以传入正则表达式用于搜索用户

**类型**: [`Contact`](contact.md#Contact)的静态方法

| 参数 | 类型 |
| :--- | :--- |
| queryArg | [`ContactQueryFilter`](contact.md#ContactQueryFilter) |

#### 示例

```python
import asyncio
from wechaty import Wechaty
from wechaty_puppet import ContactQueryFilter

class MyBot(Wechaty):

    async def on_login(self, payload) -> None:
        contact = await self.Contact.find_all()  # 获取一个列表, 里面包含了Bot所有的联系人
        contact = await self.Contact.find_all(ContactQueryFilter(name="lijiarui"))  # 获取一个包含所有名字为lijiarui的联系人的列表
        contact = await self.Contact.find_all(ContactQueryFilter(alias="ruirui"))   # 获取一个包含所有别名(备注)为ruirui的联系人的列表

asyncio.run(MyBot().start())
```
## Typedefs 类型定义

### [ContactQueryFilter](contact.md#ContactQueryFilter) 

用于搜索联系人对象的一个封装结构

| **属性名** | 类型     | **描述**                                                     |
| ---------- | -------- | ------------------------------------------------------------ |
| name       | `str` | 由用户本身(user-self)设置的名字, 叫做name                    |
| alias      | `str` | 由Bot为联系人设置的名字(备注/别名). 该值可以传入正则表达式用于搜索用户, 更多细节详见[issues#365](https://github.com/wechaty/wechaty/issues/365) |
