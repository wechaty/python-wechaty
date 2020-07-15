# 介绍

## Wechaty 是什么

微信个人号功能非常强大和灵活，是一个非常适合用来做ChatBot的载体。它可以灵活不受限制的发送语音短信、视频、图片和文字，支持多人群聊。但是使用微信个人微信号作为ChatBot，需要通过非官方的第三方库接入微信。因为截至2018年底，微信尚无任何官方的ChatBot API发布。

Python-Wechaty 是一个开源的的 个人号 微信机器人接口，是一个使用Python构建的轻量级应用，同时支持Linux, Windows, Darwin(OSX/Mac) 和 Docker 多个平台，目前支持Donut协议，申请Token请移驾

在GitHub上可以找到很多支持微信个人号接入的第三方类库，其中大多都是基于Web Wechat的API来实现的，而Python-Wechaty是基于Window下Donut协议，少数支持非Web协议的库，大多是商业私有闭源的，Wechaty是少有的开源项目支持非Web协议的类库。

只需要6行代码，你就可以 通过个人号 搭建一个 微信机器人功能 ，用来自动管理微信消息。
