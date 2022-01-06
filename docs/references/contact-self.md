---
title: ContactSelf
---

机器人本身被封装为一个`ContactSelf`类。 这个类继承自联系人`Contact`类。

## ContactSelf

机器人本身被封装为一个`ContactSelf`类。

> 提示: 这个类继承自联系人`Contact`类。

**类型**: 公共类

* [ContactSelf](contact-self.md#contactself)
  * [intance](contact-self.md#contactself)
    * [contactSelf.avatar\(\[file\]\) ⇒ `None | FileBox`](contact-self.md#contactselfavatarfile-⇒-promise)
    * [contactSelf.qrcode\(\) ⇒ `str`](contact-self.md#contactselfqrcode-⇒-promise)
    * [contactSelf.signature\(signature\) ⇒ `str`](contact-self.md#contactselfsignaturesignature)
    * [contactSelf.name\(\[name\]\) ⇒ `None | str`](contact-self.md#contactselfname-⇒-promisestring)

### contactSelf.avatar\(\[file\]\) ⇒ `None | FileBox`

获取/设置 机器人所使用账号的头像

**类型**: [`ContactSelf`](contact-self.md#ContactSelf)类的实例方法

| 参数 | 类型 |
| :--- | :--- |
| \[file\] | `FileBox` |

**示例** 

_\( 获取机器人账号的头像, 返回`FileBox`类型的对象\)_

```python
# 保存头像到本地文件, 类似 `1-name.jpg`的格式
import asyncio
from wechaty import Wechaty, FileBox, Contact

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        print(f"用户{contact}登入")
        file: FileBox = await contact.avatar()
        name = file.name
        await file.to_file(name, True)
        print(f"保存头像: {contact.name} 和头像文件: {name}")


asyncio.run(MyBot().start())
```

**示例** 

_\(设置机器人账号的头像\)_

```python
import asyncio
from wechaty import Wechaty, FileBox, Contact

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        print(f"用户{contact}登入")
        file_box: FileBox = FileBox.from_url('https://wechaty.github.io/wechaty/images/bot-qr-code.png')
        await contact.avatar(file_box)
        print(f"更改账号头像成功")


asyncio.run(MyBot().start())
```

### contactSelf.qrcode\(\) ⇒ `str`

获取机器人账号的二维码链接

**类型**: [`ContactSelf`](contact-self.md#ContactSelf)的实例方法

#### 示例

```python
import asyncio
from wechaty import Wechaty
from wechaty.user import ContactSelf
from wechaty.utils.qrcode_terminal import qr_terminal_str

class MyBot(Wechaty):

    async def on_login(self, contact: ContactSelf) -> None:
        print(f"用户{contact}登入")
        qr_code = await contact.qr_code()  # 获取二维码信息
        print(qr_terminal_str(qr_code)) # 在控制台打印二维码

asyncio.run(MyBot().start())
```

### contactSelf.signature\(signature\) ⇒ `None`

更改机器人账号的签名

**类型**: [`ContactSelf`](contact-self.md#ContactSelf)的实例方法

| 参数 |  类型 | 描述 |
| :--- | :--- | :--- |
| signature | `str` | 您想要改变的新的签名 |

#### 示例

```python
import sys
import asyncio
from datetime import datetime
from wechaty import Wechaty
from wechaty.user import ContactSelf

class MyBot(Wechaty):

    async def on_login(self, contact: ContactSelf) -> None:
        print(f"用户{contact}登入")
        try:
            await contact.signature(f"签名被Wechaty更改于{datetime.now()}")
        except Exception as e:
            print("更改签名失败", e, file=sys.stderr)

asyncio.run(MyBot().start())
```

### contactSelf.name\(\[name\]\) ⇒ `None | str`

获取或者更改机器人的名字

**类型**: [`ContactSelf`](contact-self.md#contactself)的实例方法

| 参数 | 描述 |
| :--- | :--- |
| \[name\] | 想让账号更改的新的别名 |

#### 示例

```python
import sys
import asyncio
from datetime import datetime
from wechaty import Wechaty
from wechaty.user import ContactSelf


class MyBot(Wechaty):

    async def on_login(self, contact: ContactSelf) -> None:
        old_name = contact.name
        try:
            contact.name = f"{old_name}{datetime.now()}"
        except Exception as e:
            print("更改名字失败", e, file=sys.stderr)

asyncio.run(MyBot().start())
```
