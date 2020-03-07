# python-wechaty

![PyPI Version](https://img.shields.io/pypi/v/wechaty?color=blue)
[![Downloads](https://pepy.tech/badge/wechaty)](https://pepy.tech/project/wechaty)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
![PyPI GitHub Actions](https://github.com/wechaty/python-wechaty/workflows/PyPI/badge.svg)
<!--
![PyPI - Downloads](https://img.shields.io/pypi/dm/wechaty?color=blue)
-->

![Python Wechaty](https://wechaty.github.io/python-wechaty/images/python-wechaty.png)

## Connecting Chatbots

Wechaty is a RPA SDK for Wechat **Individual** Account that can help you create a chatbot in 6 lines of Python.

## WORK IN PROGRESS

Work in progress...

Please come back after 4 weeks...

## Voice of the Developers

> "Wechaty is a great solution, I believe there would be much more users recognize it." [link](https://github.com/chatie/wechaty/pull/310#issuecomment-285574472)  
> -- @Gcaufy, Tencent Engineer, Author of [WePY](https://github.com/Tencent/wepy)

> "太好用，好用的想哭"  
> -- @xinbenlv, Google Engineer, Founder of HaoShiYou.org

> "最好的微信开发库" [link](http://weibo.com/3296245513/Ec4iNp9Ld?type=comment)  
> -- @Jarvis, Baidu Engineer

> "Wechaty让运营人员更多的时间思考如何进行活动策划、留存用户，商业变现" [link](http://mp.weixin.qq.com/s/dWHAj8XtiKG-1fIS5Og79g)  
> -- @lijiarui, CEO of BotOrange.

> "If you know js ... try Chatie/wechaty, it's easy to use."  
> -- @Urinx Uri Lee, Author of [WeixinBot(Python)](https://github.com/Urinx/WeixinBot)

See more at [Wiki:Voice Of Developer](https://github.com/Chatie/wechaty/wiki/Voice%20Of%20Developer)

## Join Us

Wechaty is used in many ChatBot projects by thousands of developers. If you want to talk with other developers, just scan the following QR Code in WeChat with secret code _python wechaty_, join our **Wechaty Python Developers' Home**.

![Wechaty Python Developers' Home](https://wechaty.github.io/wechaty/images/bot-qr-code.png)

Scan now, because other Wechaty Python developers want to talk with you too! (secret code: _python wechaty_)

## The World's Shortest Python ChatBot: 6 lines of Code

```python
from wechaty import Wechaty

Wechaty.instance() // Global Instance
  .on('scan', lambda qrcode, status : print('Scan QR Code to login: {}\nhttps://api.qrserver.com/v1/create-qr-code/?data={}'.format(status, encodeURIComponent(qrcode))))
  .on('login', lambda user: print('User {} logined'.format(user)))
  .on('message', lambda message: print('Message: {}'.format(message)))
  .start()
```

## Requirements

1. Python 3.7 or above

## Install

```shell
pip3 install wechaty
```

## Usage

WIP...

## See Also

- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)

### Static & Instance of Class

- [Static variables and methods in Python](https://radek.io/2011/07/21/static-variables-and-methods-in-python/)

### Typings

- [PEP 526 -- Syntax for Variable Annotations - Class and instance variable annotations](https://www.python.org/dev/peps/pep-0526/#class-and-instance-variable-annotations)
  - [Python Type Checking (Guide)](https://realpython.com/python-type-checking/) by [Geir Arne Hjelle](https://realpython.com/team/gahjelle/)

## Author

[Huan LI](https://github.com/huan) ([李卓桓](http://linkedin.com/in/zixia)) zixia@zixia.net

[![Profile of Huan LI (李卓桓) on StackOverflow](https://stackexchange.com/users/flair/265499.png)](https://stackexchange.com/users/265499)

## Copyright & License

- Code & Docs © 2020-now Huan LI \<zixia@zixia.net\>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons

