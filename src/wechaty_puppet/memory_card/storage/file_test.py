import pytest
import random
import asyncio

from wechaty_puppet.memory_card.storage.backend_config import StorageBackendOptionsBase, StorageFile


class TestFile:

    def test_file(self):
        EXPECTED_PAYLOAD = {'mol': 42}
        NAME = str(random.random())[2:]
        file = StorageFile(NAME, StorageBackendOptionsBase())

        empty = asyncio.run(file.load())
        assert empty == {}, 'should get back a empty object for non-exist data'

        asyncio.run(file.save(EXPECTED_PAYLOAD))
        payload = asyncio.run(file.load())

        assert payload == EXPECTED_PAYLOAD, 'should get back data from s3'

        asyncio.run(file.destroy())

        empty = asyncio.run(file.load())
        assert empty == {}, 'should get back a empty object after destroy()'

