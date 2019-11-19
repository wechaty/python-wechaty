# python-wechaty

[![Downloads](https://pepy.tech/badge/wechaty)](https://pepy.tech/project/wechaty)
[![Downloads](https://pepy.tech/badge/wechaty/month)](https://pepy.tech/project/wechaty)

Python Wechaty

![Python Wechaty](https://wechaty.github.io/wechaty/images/python-wechaty.png)

## WORK IN PROGRESS

Work in progress...

Please come back after 4 weeks...

## CONNECTING CHATBOTS

Wechaty is a Bot SDK for Wechat **Personal** Account which can help you create a bot in 6 lines of Python.

## VOICE OF THE DEVELOPER

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

## The World's Shortest Python ChatBot: 6 lines of Code

```python
from wechaty import Wechaty

Wechaty.instance() // Global Instance
.on('scan', lambda qrcode, status : print('Scan QR Code to login: {}\nhttps://api.qrserver.com/v1/create-qr-code/?data={}'.format(status, encodeURIComponent(qrcode))))
.on('login', lambda user: print('User {} logined'.format(user)))
.on('message', lambda message: print('Message: {}'.format(message)))
.start()
```

## REQUIREMENTS

1. Python 3.6 or above

## INSTALL

```shell
pip3 install wechaty
```

## USAGE

WIP...

## SEE ALSO

- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)

## AUTHOR

[Huan LI](http://linkedin.com/in/zixia) \<zixia@zixia.net\>

<a href="https://stackexchange.com/users/265499">
  <img src="https://stackexchange.com/users/flair/265499.png" width="208" height="58" alt="profile for zixia on Stack Exchange, a network of free, community-driven Q&amp;A sites" title="profile for zixia on Stack Exchange, a network of free, community-driven Q&amp;A sites">
</a>

## COPYRIGHT & LICENSE

* Code & Docs © 2018 Huan LI \<zixia@zixia.net\>
* Code released under the Apache-2.0 License
* Docs released under Creative Commons
