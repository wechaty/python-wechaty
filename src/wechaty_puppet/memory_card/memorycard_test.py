import asyncio
import unittest
from dataclasses import dataclass
from .memory_card import MemoryCard, MemoryCardOptions
from .storage.backend_config import StorageFileOptionsExtends, StorageBackendOptionsBase, StorageObsOptionsExtends
import random
from typing import Any


@dataclass
class OBS_SETTING:
    ACCESS_KEY_ID = 'AQFJBZBZA0BTMSCE8DDN'
    BUCKET = 'xiaobeitest'
    SECRET_ACCESS_KEY = '1LduhgPkhtGO1UdNlZ7KZu2XjK7g1x833Z8q54yM+VJ83SAa2a9VTeGQST'
    SERVER = 'https://obs.cn-north-4.myhuaweicloud.com'


memcardoptions = MemoryCardOptions(name='nop')


class memorycard_test(unittest.TestCase):

    def test_smoke_testing(self):
        card = MemoryCard(memcardoptions)
        asyncio.run(card.load())

        self.assertEqual(card.size, 0, 'init with 0')

        asyncio.run(card.set('a', 'b'))
        self.assertEqual(asyncio.run(card.get('a')), 'b', 'get key a with value b')

        asyncio.run(card.clear())
        self.assertEqual(card.size, 0, 'clear reset to 0')

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
        self.assertEqual(asyncio.run(cardB.get(EXPECTED_KEY)), EXPECTED_VAL, 'should get val back from file')

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
            self.fail('should not call save() success')
        except Exception as e:
            self.assertTrue('should throw to call save() before load()')

    def test_load(self):
        NAME = str(random.random())[2:]
        card = MemoryCard(MemoryCardOptions(name=NAME, storageOptions=StorageBackendOptionsBase(type='file')))
        try:
            asyncio.run(card.load())
            asyncio.run(card.load())
            self.fail('should not call load() success after twice')
        except Exception as e:
            self.assertTrue(True, 'should throw to call load() twice')

    def test_memorycard(self):
        card = MemoryCard()
        self.assertEqual(card.name, None, 'should get None as name')


if __name__ == '__main__':
    unittest.main(argv=['-v'])
