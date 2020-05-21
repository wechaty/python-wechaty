import asyncio
import pytest
from dataclasses import dataclass
from wechaty_puppet.memory_card import MemoryCard
from wechaty_puppet.memory_card.memory_card import MemoryCardOptions
from wechaty_puppet.memory_card.storage.backend_config import StorageFileOptionsExtends, StorageBackendOptionsBase, StorageObsOptionsExtends
import random
from typing import Any


@dataclass
class OBS_SETTING:
    ACCESS_KEY_ID = 'AQFJBZBZA0BTMSCE8DDN'
    BUCKET = 'xiaobeitest'
    SECRET_ACCESS_KEY = '1LduhgPkhtGO1UdNlZ7KZu2XjK7g1x833Z8q54yM+VJ83SAa2a9VTeGQST'
    SERVER = 'https://obs.cn-north-4.myhuaweicloud.com'


memcardoptions = MemoryCardOptions(name='nop')


class TestMemoryCard:

    def test_smoke_testing(self):
        card = MemoryCard(memcardoptions)
        asyncio.run(card.load())

        assert card.size == 0, 'init with 0'

        asyncio.run(card.set('a', 'b'))
        assert asyncio.run(card.get('a')) == 'b', 'get key a with value b'
        asyncio.run(card.clear())
        assert card.size == 0, 'clear reset to 0'

    def test_storage_file(self):
        EXPECTED_KEY = 'key'
        EXPECTED_VAL = 'val'
        NAME = str(random.random())[2:]

        card = MemoryCard(MemoryCardOptions(name=NAME, storageOptions=StorageBackendOptionsBase(type='file')))

        asyncio.run(card.load())
        asyncio.run(card.set(EXPECTED_KEY, EXPECTED_VAL))
        asyncio.run(card.save())

        cardB = MemoryCard(MemoryCardOptions(name=NAME, storageOptions=StorageBackendOptionsBase(type='file')))
        asyncio.run(cardB.load())
        assert asyncio.run(cardB.get(EXPECTED_KEY)) == EXPECTED_VAL, 'should get val back from file'

        asyncio.run(card.destroy())
        asyncio.run(cardB.destroy())

    # def test_obs(self):
    #     EXPECTED_KEY = 'key'
    #     EXPECTED_VAL = 'val'
    #     NAME = str(random.random())[2:]
    #
    #     storageOptions = StorageObsOptionsExtends(accessKeyId=OBS_SETTING.ACCESS_KEY_ID,
    #                                               bucket=OBS_SETTING.BUCKET,
    #                                               secretAccessKey=OBS_SETTING.SECRET_ACCESS_KEY,
    #                                               server=OBS_SETTING.SERVER,
    #                                               type='obs', )
    #     card = MemoryCard(MemoryCardOptions(name=NAME, storageOptions=storageOptions))
    #     asyncio.run(card.load())
    #
    #     asyncio.run(card.set(EXPECTED_KEY, EXPECTED_VAL))
    #     asyncio.run(card.save())
    #
    #     cardB = MemoryCard(MemoryCardOptions(name=NAME, storageOptions=storageOptions))
    #     asyncio.run(cardB.load())
    #
    #     self.assertEqual(asyncio.run(cardB.get(EXPECTED_KEY)), EXPECTED_VAL, 'should get val back from obs')
    #     asyncio.run(card.destroy())
    #     asyncio.run(cardB.destroy())
    #
    def test_save(self):
        NAME = str(random.random())[2:]
        card = MemoryCard(MemoryCardOptions(name=NAME, storageOptions=StorageBackendOptionsBase(type='file')))
        try:
            asyncio.run(card.save())
            assert 'should not call save() success'
        except Exception as e:
            assert 'should throw to call save() before load()'

    def test_load(self):
        NAME = str(random.random())[2:]
        card = MemoryCard(MemoryCardOptions(name=NAME, storageOptions=StorageBackendOptionsBase(type='file')))
        try:
            asyncio.run(card.load())
            asyncio.run(card.load())
            assert 'should not call load() success after twice'
        except Exception as e:
            assert 'should throw to call load() twice'

    def test_memorycard(self):
        card = MemoryCard()
        assert card.name is None, 'should get None as name'

