# python-wechaty 能登录多个微信吗？

可以。必须保证一个进程内只启动一个wechaty实例，可通过多行命令来启动多个wechaty实例，或在程序当中使用多进程启动多个wechaty实例（不推荐）。