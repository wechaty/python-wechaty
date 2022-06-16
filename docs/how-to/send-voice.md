---
title: "如何生成&发送语音"
---

# 介绍

目前python-wechaty已完成audio 消息类型的测试，本文档包含如下内容：

* 安装
* 发送语音文件
* 将wav/mp3等其它类型文件转化成silk语音文件
* 使用paddlespeech生成语音

# 安装

```shell
pip install wechaty

pip install wechaty-puppet>=0.4.19
```

注意点：需要保证`wechaty-puppet`的版本`>=0.4.19`。

# 发送语音文件

```python
async def on_message(self, msg: Message) -> None:
    """listen message event"""
    if msg.room():
        return

    if msg.type() == MessageType.MESSAGE_TYPE_AUDIO:
        # 保存用户发送的语音文件
        file_box = await msg.to_file_box()
        saved_file = os.path.join(self.cache_dir, file_box.name)
        await file_box.to_file(saved_file)

        # 将本地保存的语音文件发送给说话者
        new_audio_file = FileBox.from_file(saved_file)
        new_audio_file.metadata = {
            "voiceLength":2000
        }
        await msg.talker().say(new_audio_file)
```

# 生成silk语音文件

此过程使用[Python-Silk-Module](https://github.com/DCZYewen/Python-Silk-Module) 来完成silk语音文件的生成，操作非常简单，有手就会：

```python
import pysilk

# 编码部分，输出silk
#pysilk.encode(pcm_data: bytes, data_rate=24000)
pysilk.encode_file(open("mopemope.pcm", "rb"), 24000)
# 解码部分，输出pcm
# to_wav为True时输出wav文件
#pysilk.decode(silk_data: bytes, to_wav = False)
pysilk.decode_file(open("brainpower.pcm", "rb"), to_wav=False)
```

# 根据文本生成音频文件

此过程推荐使用[paddlespeech](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/streaming_tts_server)直接**根据文本生成wav音频文件**，然后使用`pysilk`转化成可发送的目标音频文件。

给大家推荐一个宝藏Repo： [PaddleSpeechDemo](https://github.com/iftaken/PaddleSpeechDemo)，此作者为届时PaddleSpeech PM，目前处于开发阶段，以后也会持续更新，有需求的小伙伴可以持续关注。
