Python Wechaty Contribution Guide
=================================

## Introduction

Welcome to python-wechaty, contributors.

In order to help everyone start easier, and understand our project faster, we wrote this documentation.

## Request your donut (hostie) token

Now python-wechaty only supports donut puppet. So before you start, you should request a token for `wechaty-puppet-hostie` first.

You can follow either of the two issues below to request a donut token:

* [wechaty#1941 - \[Call for Volunteers\] Win32 Puppets: wechaty-puppet-donut is going to ready for testing!](https://github.com/wechaty/wechaty/issues/1941)
* [wechaty#1986 - How to create your own Wechaty Hostie Token with the Web Protocol](https://github.com/wechaty/wechaty/issues/1986)

## Start your own demo bot project

After you get your own hostie token, you can clone the demo project and start writing your bot.

* <https://github.com/wechaty/python-wechaty-getting-start>

So now you can try python-wechaty freely. Install the PyPI requirements will install all the `python-wechaty` relevant packages in your environment.

## Knowing about the relevant repositories about `python-wechaty` in our group

Before we start to contribute on `python-wechaty`, we should know about the repositories we are working on.

After you finish the installation of the PyPI requirements, you will soon find out some relative python packages, I will introduce one by one later.

But before you start, please read more about the [Python Wechaty Architecture Diagram](https://github.com/wechaty/python-wechaty/issues/9)

### 1. python-wechat

* GitHub: <https://github.com/wechaty/python-wechaty>
* PyPI: <https://pypi.org/project/wechaty/> [![PyPI Version](https://img.shields.io/pypi/v/wechaty?color=blue)](https://pypi.org/project/wechaty)

This repository is actually what you are using in your bot project, it is independent about the puppet you choose (hostie/padplus/other). Although, we only supports hostie puppet now, but more puppet supports will be added later.

When you login your bot, in fact your wechat account is running in the puppet server, and you listen events from the puppet-server, and send action to the puppet-server. Our python-wechat is a SDK project to let you access the puppet-server easier.

### 2. python-wechaty-puppet

* GitHub: <https://github.com/wechaty/python-wechaty-puppet>
* PyPI: <https://pypi.org/project/wechaty-puppet/> [![PyPI Version](https://img.shields.io/pypi/v/wechaty-puppet?color=blue)](https://pypi.org/project/wechaty-puppet)

Wechaty has different puppet implementations, see:

> <https://github.com/Wechaty/wechaty-puppet/wiki/Directory>

And our `python-wechat` is designed be able to plug to any of them (for now, implements `wechaty-puppet-hostie` only)

But different puppet shares some common protocol, so before we write a `python-puppet` implementation, we should have this abstract base class. 

This repository defines all method signatures and specified payload formats about how to communicate with the puppet-server.

When the `python-wechaty` want to call a RPC method to puppet-server, it calls the methods defined in `python-wechat-puppet`, but the method implementation is not here, you should find them under the puppet implementation project, which we are about to show next.

### 3. python-wechaty-puppet-hostie

* GitHub: <https://github.com/wechaty/python-wechaty-puppet-hostie>
* PyPI: <https://pypi.org/project/wechaty-puppet-hostie/> [![PyPI Version](https://img.shields.io/pypi/v/wechaty-puppet-hostie?color=blue)](https://pypi.org/project/wechaty-puppet-hostie)

So, the `python-wecahty-puppet-hostie` implements the methods defined in `python-wechaty-puppet`, which are used in the `python-wechaty`.

If you want to debug the actual call to the puppet server, here is where you've been looking for.

Finding the puppet method in the `python-wechaty` project will lead you to the `wecahty_puppet` package in your IDE, you can follow the method overrides to find the implementation in you IDE, it will lead you here.

### 4. chatie_grpc

* GitHub: <https://github.com/Chatie/grpc>
* PyPI: <https://pypi.org/project/chatie_grpc/> [![PyPI Version](https://img.shields.io/pypi/v/chatie_grpc?color=blue)](https://pypi.org/project/wechaty-puppet-hostie)

So if you look into the `puppet_stub` method in the `python-wechaty-puppet-hostie` project, you will find the `chatie_grpc` package.

This package is auto generated from the grpc Protocol Buffer project, which defines all api format to the puppet-server.

You are suggested to modify the grpc project rarely, but you can get much valuable information about the api in the grpc project code, like the payload field definitions, and also the enum constant values.

### 5. python-wechaty-plugin-contrib

* GitHub: <https://github.com/wechaty/python-wechaty-plugin-contrib>

Here collects the plugins developed by the community. If you want to publish your own plugin, feel free to make a PR on it.

This repository is less relevant to the python-wecahty core, so if you want to focus on the core function, you can skip this one freely.

## One practise to work within PyCharm IDE

So, you have already forked the `python-wechaty-getting-started` project or created your own bot project, and the PyPI packages mentioned above is installed by the `pip install` way.

Now we start to have a discuss on how to work easier in your IDE.

Here we show a working practise in PyCharm IDE, if you have a better way, or want to share your instruction under other development environment, feel free to make a PR.

### 1. Set a python virtual environment for the bot project

### 2. Add the WECHATY_PUPPET_HOSTIE_TOKEN environment params

### 3. Add the python-wechaty repositories as git submodules

### 4. Mark these src directory as source

### 5. Change the code and push to your own fork version

### 6. Make a PR (pull request) in GitHub
