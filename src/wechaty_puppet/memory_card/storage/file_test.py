import unittest
import random
import asyncio

from wechaty_puppet.memory_card.storage.backend_config import StorageBackendOptionsBase, StorageFile


class filetest(unittest.TestCase):

    def test_file(self):
        EXPECTED_PAYLOAD = {'mol': 42}
        NAME = str(random.random())[2:]
        file = StorageFile(NAME, StorageBackendOptionsBase())

        empty = asyncio.run(file.load())
        self.assertEqual(empty, {}, 'should get back a empty object for non-exist data')

        asyncio.run(file.save(EXPECTED_PAYLOAD))
        payload = asyncio.run(file.load())

        self.assertEqual(payload, EXPECTED_PAYLOAD, 'should get back data from s3')

        asyncio.run(file.destroy())

        empty = asyncio.run(file.load())
        self.assertEqual(empty, {}, 'should get back a empty object after destroy()')


if __name__ == '__main__':
    unittest.main(argv=['-v'])
