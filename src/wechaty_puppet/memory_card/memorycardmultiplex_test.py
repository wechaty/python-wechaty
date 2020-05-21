"""doc"""
import pytest
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


class TestMemoryCardMultiplex:

    def test_multiplex_set(self):
        KEY = 'a'
        VAL = 'b'
        NAME = str(random.random())[2:]

        card = MemoryCard(MemoryCardOptions(name=NAME))
        asyncio.run(card.load())

        cardA = card.multiplex_copy('a')
        cardB = card.multiplex_copy('b')

        assert card.size == 0, 'init with 0 for card'
        assert cardA.size == 0, 'init with 0 for cardA'
        assert cardB.size == 0, 'init with 0 for cardB'

        asyncio.run(card.set(KEY, VAL))
        assert card.size == 1, 'size with 1'
        assert cardA.size == 0, 'size with 0 for cardA'
        assert cardB.size == 0, 'size with 0 for cardB'

        asyncio.run(cardA.set(KEY, VAL))
        assert card.size == 2, 'card size with 2(include cardA)'
        assert cardA.size == 1, 'cardA size with 1'
        assert cardB.size == 0, 'cardB size with 0'

        asyncio.run(cardB.set(KEY, VAL))
        assert card.size == 3, 'card size with 3(include cardA & cardB)'
        assert cardA.size == 1, 'cardA size with 1'
        assert cardB.size == 1, 'cardB size with 1'

        asyncio.run(cardB.delete('a'))
        assert card.size == 2, 'card size with 2(include cardA)'
        assert cardA.size == 1, 'cardA size with 1'
        assert cardB.size == 0, 'cardB size with 0'

        asyncio.run(cardA.delete('a'))
        assert card.size == 1, 'size with 1'
        assert cardA.size == 0, 'size with 0 for cardA'
        assert cardB.size == 0, 'size with 0 for cardB'

        asyncio.run(card.delete('a'))
        assert card.size == 0, 'init with 0 for card'
        assert cardA.size == 0, 'init with 0 for cardA'
        assert cardB.size == 0, 'init with 0 for cardB'

        asyncio.run(card.destroy())

    def test_multiplex_clear(self):
        KEY = 'a'
        VAL = 'b'
        NAME = str(random.random())[2:]

        card = MemoryCard(MemoryCardOptions(name=NAME))
        asyncio.run(card.load())

        cardA = card.multiplex_copy('a')
        cardB = card.multiplex_copy('b')

        asyncio.run(card.set(KEY, VAL))
        asyncio.run(cardA.set(KEY, VAL))
        asyncio.run(cardB.set(KEY, VAL))

        assert card.size == 3, 'card size with 3(include cardA & cardB)'
        assert cardA.size == 1, 'cardA size with 1'
        assert cardB.size == 1, 'cardA size with 1'

        asyncio.run(cardB.clear())
        assert card.size == 2, 'card size with 2(include cardA & cardB)'
        assert cardA.size == 1, 'cardA size with 1'
        assert cardB.size == 0, 'cardA size with 0'

        asyncio.run(cardA.clear())
        assert card.size == 1, 'card size with 1(include cardA & cardB)'
        assert cardA.size == 0, 'cardA size with 0'
        assert cardB.size == 0, 'cardA size with 0'

        asyncio.run(card.destroy())

    def test_multiplex_deeper(self):
        KEY = 'a'
        VAL = 'b'
        NAME = str(random.random())[2:]
        card = MemoryCard(MemoryCardOptions(name=NAME))
        asyncio.run(card.load())

        cardA = card.multiplex_copy('a')
        cardAA = cardA.multiplex_copy('a')
        cardAAA = cardAA.multiplex_copy('a')

        asyncio.run(card.set(KEY, VAL))
        asyncio.run(cardA.set(KEY, VAL))
        asyncio.run(cardAA.set(KEY, VAL))
        asyncio.run(cardAAA.set(KEY, VAL))

        assert card.size == 4, 'card size with 4(include cardA & cardAA & cardAAA)'
        assert cardA.size == 3, 'cardA size with 3'
        assert cardAA.size == 2, 'cardAA size with 2'
        assert cardAAA.size == 1, 'cardAAA size with 1'

        asyncio.run(cardAA.delete("a"))
        assert card.size == 3, 'card size with 3(include cardA & cardAAA)'
        assert cardA.size == 2, 'cardA size with 2'
        assert cardAA.size == 1, 'cardAA size with 1 (include cardAAA)'
        assert cardAAA.size == 1, 'cardAAA size with 1'

        asyncio.run(card.destroy())

    def test_multiplex_destroy(self):
        NAME = str(random.random())[2:]
        card = MemoryCard(MemoryCardOptions(name=NAME))
        asyncio.run(card.load())

        cardA = card.multiplex_copy('test')
        try:
            asyncio.run(cardA.destroy())
            assert 'should throw'
        except Exception as e:
            assert 'should not allow destroy() on multiplexed memory'

    def test_multiplex_clear1(self):
        KEY = 'a'
        VAL = 'b'
        NAME = str(random.random())[2:]

        card = MemoryCard(MemoryCardOptions(name=NAME))
        asyncio.run(card.load())

        cardA = card.multiplex_copy('test')
        asyncio.run(card.set(KEY, VAL))
        asyncio.run(cardA.set(KEY, VAL))

        asyncio.run(cardA.clear())

        assert card.size == 1, 'should keep parent data when clear child(multiplex)'
        assert cardA.size == 0, 'should clear the memory'

    def test_multiplex_has(self):
        KEY = 'a'
        VAL = 'b'
        KEYA = 'aa'
        VALA = 'bb'
        NAME = str(random.random())[2:]
        card = MemoryCard(MemoryCardOptions(name=NAME))
        asyncio.run(card.load())

        cardA = card.multiplex_copy('test')
        asyncio.run(card.set(KEY, VAL))
        asyncio.run(cardA.set(KEYA, VALA))

        assert asyncio.run(card.has(KEY)) is True, 'card should has KEY'
        assert asyncio.run(card.has(KEYA)) is False, 'card should not has KEYA'

        assert asyncio.run(cardA.has(KEYA)) is True, 'card should has KEYA'
        assert asyncio.run(cardA.has(KEY)) is False, 'card should not has KEY'

        asyncio.run(card.destroy())


    # def test_multiplex_keys(self):
    #     KEY = 'a'
    #     VAL = 'b'
    #     KEYA = 'aa'
    #     VALA = 'bb'
    #     NAME = str(random.random())[2:]
    #     card = MemoryCard(MemoryCardOptions(name=NAME))
    #     asyncio.run(card.load())
    #
    #     cardA = card.multiplex_copy('test')
    #     asyncio.run(card.set(KEY, VAL))
    #     asyncio.run(cardA.set(KEYA, VALA))
    #
    #     cardKeys = []
    #     cardAKeys = []
    #
    #     for key in card.keys():
    #         cardKeys.append(key)
    #
    #     for key in cardA.keys():
    #         cardAKeys.append(key)
    #
    #     assert cardKeys, [KEY, cardA._resolveKey(KEYA)], 'should get keys back for card')
    #     assert cardAKeys, [KEYA], 'should get keys back for cardA')

