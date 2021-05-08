# 什么是Puppet

The term `Puppet`in Wechaty is an Abstract Class for implementing protocol plugins. The plugins are the component that helps Wechaty to control the Wechat(that's the reason we call it puppet).

The plugins are named XXXPuppet, like PuppetPuppeteer is using the chrome puppeteer to control the WeChat Web API via a chrome browser, PuppetPadchat is using the WebSocket protocol to connect with a Protocol Server for controlling the iPad Wechat program.

# python-wechaty 能登录多个微信吗？

可以。必须保证一个进程内只启动一个wechaty实例，可通过多行命令来启动多个wechaty实例，或在程序当中使用多进程启动多个wechaty实例（不推荐）。
