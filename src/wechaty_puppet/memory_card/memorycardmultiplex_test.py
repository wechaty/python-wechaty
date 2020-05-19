import unittest
import random
import asyncio
from .memory_card import MemoryCard, MemoryCardOptions
from .mctypes import MemoryCardPayload


class MemoryCardTest(MemoryCard):

    @property
    def payload(self):
        return super().payload

    @payload.setter
    def payload(self, data: MemoryCardPayload):
        super().payload = data

    def resolveKey(self, key: str) -> str:
        return super()._resolveKey(key)

    def multiplexPath(self) -> str:
        return super()._multiplexPath()

    def isMultiplexKey(self, key: str) -> bool:
        return super()._isMultiplexKey(key)


class memorycardmultiplextest(unittest.TestCase):

    def test_multiplex_set(self):
        KEY = 'a'
        VAL = 'b'
        NAME = str(random.random())[2:]

        card = MemoryCard(MemoryCardOptions(name=NAME))
        asyncio.run(card.load())

        cardA = card.multiplex_copy('a')
        cardB = card.multiplex_copy('b')

        self.assertEqual(card.size,  0, 'init with 0 for card')
        self.assertEqual(cardA.size,  0, 'init with 0 for cardA')
        self.assertEqual(cardB.size,  0, 'init with 0 for cardB')

        asyncio.run(card.set(KEY, VAL))
        self.assertEqual(card.size,  1, 'size with 1')
        self.assertEqual(cardA.size, 0, 'size with 0 for cardA')
        self.assertEqual(cardB.size, 0, 'size with 0 for cardB')

        asyncio.run(cardA.set(KEY, VAL))
        self.assertEqual(card.size,  2, 'card size with 2(include cardA)')
        self.assertEqual(cardA.size, 1, 'cardA size with 1')
        self.assertEqual(cardB.size, 0, 'cardB size with 0')

        asyncio.run(cardB.set(KEY, VAL))
        self.assertEqual(card.size,  3, 'card size with 3(include cardA & cardB)')
        self.assertEqual(cardA.size, 1, 'cardA size with 1')
        self.assertEqual(cardB.size, 1, 'cardB size with 1')

        asyncio.run(cardB.delete('a'))
        self.assertEqual(card.size,  2, 'card size with 2(include cardA)')
        self.assertEqual(cardA.size, 1, 'cardA size with 1')
        self.assertEqual(cardB.size, 0, 'cardB size with 0')

        asyncio.run(cardA.delete('a'))
        self.assertEqual(card.size, 1, 'size with 1')
        self.assertEqual(cardA.size, 0, 'size with 0 for cardA')
        self.assertEqual(cardB.size, 0, 'size with 0 for cardB')

        asyncio.run(card.delete('a'))
        self.assertEqual(card.size,  0, 'init with 0 for card')
        self.assertEqual(cardA.size,  0, 'init with 0 for cardA')
        self.assertEqual(cardB.size,  0, 'init with 0 for cardB')

        asyncio.run(card.destroy())


if __name__ == '__main__':
    unittest.main(argv=['-v'])
