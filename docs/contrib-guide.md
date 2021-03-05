# Python Wechaty Contribution Guide

## Introduction

Welcome to python-wechaty, contributors.

In order to help everyone start easier, and understand our project faster, we wrote this documentation.

## Request your donut (hostie) token

Now python-wechaty only supports donut puppet. So before you start, you should request a token for `wechaty-puppet-service` first.

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

And our `python-wechat` is designed be able to plug to any of them (for now, implements `wechaty-puppet-service` only)

But different puppet shares some common protocol, so before we write a `python-puppet` implementation, we should have this abstract base class.

This repository defines all method signatures and specified payload formats about how to communicate with the puppet-server.

When the `python-wechaty` want to call a RPC method to puppet-server, it calls the methods defined in `python-wechat-puppet`, but the method implementation is not here, you should find them under the puppet implementation project, which we are about to show next.

### 3. python-wechaty-puppet-service

* GitHub: <https://github.com/wechaty/python-wechaty-puppet-service>
* PyPI: <https://pypi.org/project/wechaty-puppet-service/> [![PyPI Version](https://img.shields.io/pypi/v/wechaty-puppet-service?color=blue)](https://pypi.org/project/wechaty-puppet-service)

So, the `python-wecahty-puppet-service` implements the methods defined in `python-wechaty-puppet`, which are used in the `python-wechaty`.

If you want to debug the actual call to the puppet server, here is where you've been looking for.

Finding the puppet method in the `python-wechaty` project will lead you to the `wecahty_puppet` package in your IDE, you can follow the method overrides to find the implementation in you IDE, it will lead you here.

### 4. wechaty_grpc

* GitHub: <https://github.com/wechaty/grpc>
* PyPI: <https://pypi.org/project/wechaty-grpc/> [![PyPI Version](https://img.shields.io/pypi/v/wechaty-grpc?color=blue)](https://pypi.org/project/wechaty-puppet-service)

So if you look into the `puppet_stub` method in the `python-wechaty-puppet-service` project, you will find the `wechaty-grpc` package.

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

* File \> Settings \> Project Interpreter \> Add
* Add a new virtual environment base on Python 3.7+
* Find the "Run/Debug Configuration" on the dropdown box to the left of the "Run" icon in the top-right area.
* Click "Edit Configurations..."
* Select the newly added virtual environment as the Python interpreter
* Add WECHATY_PUPPET_SERVICE_TOKEN=\<your_token\> in the "Environment variables" row
* Run `pip install -r requirements.txt` in the Terminal panel (you can see the terminal has been already working on your virtual environment automatically)
* Set the Script path to your bot.py, for example, select `ding-dong-bot.py`

Now you can run your bot by clicking the "Run" button.

### 2. Add the python-wechaty repositories as git submodules

If you want to modify the python-wechaty repository during debugging your bot, you should first replace the running code from PyPI modules to your source directory.

Here I recommend a convenient way to make it, if you are using PyCharm and run as the last step.

1. Fork the repo which you want to modify.

2. Add it into your getting-started project as a submodule.

    For example:

    ```sh
    git submodule add https://github.com/yourname/python-wechaty
    ```

    Now the remote `origin` stands for your own forked repo.

3. Add an extra remote `wechaty` as the official one:

    ```sh
    cd python-wechaty
    git remote add origin wechaty https://github.com/wechaty/python-wechaty
    ```

    So if you want to pull from the official latest changes, just use `git pull wechaty master`.

4. Set the `???/src` folder in your submodule as `Source Root` in PyCharm

So now you can change the code and have a try, the `import wechaty` of your code now points to the source you've added as a submodule.

### 4. Change the code and push to your own fork version

So feel free to change the code as your submodule and have a test.

If your are done, now you can commit the submodule and push to your forked repo (origin master).

```sh
cd python-wechaty
git commit -am "your comment"
git push origin master
```

### 5. Make a PR (pull request) in GitHub

So now you've got commits on your forked repo, feel free to request a pull-request on it.
