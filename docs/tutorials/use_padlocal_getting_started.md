# 使用Padlocal协议启动微信机器人

底层的对接实现是基于TypeScript语言，故无法直接在python-wechaty中使用该服务。可是Wechaty社区能够直接将其转化成对应的服务让多语言调用，从而实现：底层复用的特性。

整体步骤分为两步：

* 申请一个TOKEN
* 部署模板机器人


## 一、申请一个TOKEN
- 可以通过手机号注册来获得一个7天免费的TOKEN:[申请地址](http://pad-local.com)
- [TOKEN 说明](https://wechaty.js.org/docs/puppet-services/)
- 那如何获取长期Token呢？详细请看：[Everything-about-Wechaty](https://github.com/juzibot/Welcome/wiki/Everything-about-Wech aty)



## 二、 部署模板机器人

- 现在的你已经拥有了一个Padlocal Token. 接下来则需要使用它启动我们的第一个机器人了。
- 在这里，我们直接使用[python-wechaty-template](https://github.com/wechaty/python-wechaty-template)项目来快速的部署我们的第一个机器人。
- **在此之前请确保你的机器上已经安装并运行了[docker](https://www.docker.com/get-started)服务**

### 1. clone 模板机器人项目

```she
git clone https://github.com/wechaty/python-wechaty-template && cd python-wechaty-template
```

### 2. 启动padlocal网关

- 参数为申请的token，下面示例中token不可用，请换上你申请的token

```shel
./start_gateway_docker.sh puppet_padlocal_d764cc8d231747b18b9ee5540dadd55c
```

### 3. 启动机器人

- 上一步会启动一个docker，并运行Gateway服务，会有持续输出，建议运行在tmux中。
- 开起一个新的terminal，并在模板机器人项目路径下运行以下命令

```shell
make bot
```

- 初次登陆时，可能需要扫码多次。

### 4. 验证机器人启动成功

- 机器人发送消息`ding`来测试，如果启动成功，则机器人自动回复`dong`，至此你的第一个微信机器人就启动成功了。





##  三、自定义配置



### 3.1 使用docker启动的padlocal网关参数说明

- 这些参数在模板机器人项目中的`start_gateway_docker.sh`脚本中配置

* **WECHATY_PUPPET**: **标识**使用的哪个协议，一般和`token`类型的一一对应。比如当使用`padlocal`协议的话，那这个就是`wechaty-puppet-padlocal`，如果使用`web`协议的话，那这个就是`wechaty-puppet-wechat`。
* **WECHATY_PUPPET_PADLOCAL_TOKEN**: 这个协议是用来连接Padlocal的服务，目前是付费的。也就是在第一步中申请的。
* **WECHATY_PUPPET_SERVER_PORT**: 网关服务的接口，提供给`python-wechaty`来连接调用，如果服务部署在云服务器上，则需要保证该端口的可访问性。（默认8080）
* **WECHATY_TOKEN**: 当开发者在自己机器上启动一个网关服务时，需要通过`TOEKN`来做身份验证，避免服务被他人窃取。脚本中使用uuid自动生成。具体值可在`.env`文件中查看

网关服务启动成功之后，只需要编写`python-wechaty`的代码来连接即可。



## 四、使用python-wechaty连接远程网关服务

### 4.1 本地测试和远端部署

当启动网关服务时，`Padlocal`会根据`WECHATY_TOKEN`来在[Wechaty服务接口](https://api.chatie.io/v0/hosties/__TOKEN__)上注册部署机器的`IP`和`端口`，然后python-wechaty会根据`WECHATY_TOKEN`在[Wechaty服务接口](https://api.chatie.io/v0/hosties/__TOKEN__)上获取对应的IP和端口。

可是很多小伙伴在实际开发的过程中，通常会出现`endpoint is not invalid`等错误信息，那是因为开发者有可能在本地启动网关服务或者服务器端口没有开放。

网关服务的部署通常是分为本地测试和远端部署，前者通常只是为了初学测试，后者是为了生产部署。如果是在生产部署时，只需要将模板机器人项目下的.env文件内容在本地保持一致即可。即使用gateway启动时生成的token即可在本地访问远程网关服务。

### 4.2 TOKEN的作用

总而言之:

* 如果是公网环境下，可只需要设置`TOKEN`即可（因为你的token已经注册在chatie server上，故可以获取到目标资源服务器的ip和port）
* 如果是内网环境下，可只需要使用`ENDPOINT`(`localhost:port`)来让python-wechaty连接目标资源服务器。

> 如果是token是padlocal类型，则在python-wechaty程序内部可直接设置`export endpoint=localhost:port`来连接Gateway Server。
