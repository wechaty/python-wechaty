"""doc"""
from __future__ import annotations
import logging
import json
import re
from typing import (
    Optional,
    List,
)

from dataclasses import dataclass
import asyncio
from .config import VERSION
from .storage import (
    getStorage,
    StorageBackend,
    StorageBackendOptions
)
from .mctypes import (
    AsyncMap,
    MemoryCardPayload
)

log = logging.getLogger('memory_card')
NAMESPACE_MULTIPLEX_SEPRATOR = '\r'
NAMESPACE_KEY_SEPRATOR = '\n'
# TODO?
NAMESPACE_MULTIPLEX_SEPRATOR_REGEX = re.compile(NAMESPACE_MULTIPLEX_SEPRATOR)
NAMESPACE_KEY_SEPRATOR_REGEX = re.compile(NAMESPACE_KEY_SEPRATOR)


@dataclass
class multiplexprop:
    parent: MemoryCard
    name: str


@dataclass
class MemoryCardOptions:
    # TODO name: Optional[str]
    name: Optional[str] = None
    storageOptions: Optional[StorageBackendOptions] = None
    multiplex: Optional[multiplexprop] = None


@dataclass
class MemoryCardJsonObject:
    payload: MemoryCardPayload
    options: MemoryCardOptions


# TODO
class MemoryCard(AsyncMap):
    VERSION = VERSION

    @staticmethod
    def fromJSON(textOrObj) -> MemoryCard:
        log.info('MemoryCard', 'fromJSON(...)')
        jsonObj: MemoryCardJsonObject
        if type(textOrObj) == str:
            jsonObj = json.loads(textOrObj)
        else:
            jsonObj = textOrObj
        card = MemoryCard(jsonObj.options)
        return card

    @classmethod
    def multiplex(cls, name: str, memory: MemoryCard) -> MemoryCard:
        log.info('MemoryCard', 'static multiplex(%s, %s)' % (memory, name))
        memorycard = MemoryCardOptions(storageOptions=memory.options, multiplex=multiplexprop(name=name, parent=memory))
        mpMemory = cls(memorycard)
        return mpMemory

    name: Optional[str] = None

    parent: Optional[MemoryCard] = None
    payload: Optional[MemoryCardPayload] = None
    storage: Optional[StorageBackend] = None
    multiplexNameList = List[str]

    options: Optional[MemoryCardOptions] = None

    def __init__(self, options: Optional[MemoryCardOptions] = None):
        super().__init__()
        # log.info('MemoryCard', 'constructor(%s)' % json.dumps(options))

        if type(options) == str:
            options = MemoryCardOptions(name=options)

        self.options = options
        self.name = options and options.name

        if options and options.multiplex:
            self.parent = options.multiplex.parent
            self.payload = self.parent.payload
            self.multiplexNameList = [
                *self.parent.multiplexNameList,
                options.multiplex.name,
            ]
            self.storage = None
        else:
            self.payload = None

            self.multiplexNameList = []
            self.storage = self.__getStorage()

    def toString(self):
        mpString = ""
        if len(self.multiplexNameList) > 0:
            mpString = ''.join(map(lambda multiplexName: ".multiplex" + multiplexName, self.multiplexNameList))

        name = str(self.options.name) if (self.options and self.options.name) else ""

        return "MemoryCard <{0} >{1}".format(name, mpString)

    @property
    def version(self) -> str:
        return VERSION

    def __getStorage(self):
        log.info('MemoryCard', 'getStorage() for storage type: %s',
                 (self.options
                  and self.options.storageOptions
                  and self.options.storageOptions.type
                  ),  # |'N/A'
                 )
        if not self.options:
            return
        storage = getStorage(self.options.name, self.options.storageOptions)
        return storage

    async def load(self):
        log.info('MemoryCard', 'load() from storage: %s' % self.storage)  # |'N/A'
        if self.isMultiplex():
            log.warning('MemoryCard', 'load() should not be called on a multiplex MemoryCard. NOOP')
            return
        if self.payload:
            raise Exception('memory had already loaded before.')

        if self.storage:
            self.payload = await self.storage.load()
        else:
            log.info('MemoryCard', 'load() no storage')
            self.payload = {}

    async def save(self):
        if self.isMultiplex():
            if not self.parent:
                raise Exception('multiplex memory no parent')
            return self.parent.save()

        log.info('MemoryCard', '<%s>%s save() to %s' % (self.name and '', self._multiplexPath(),
                                                        self.storage and None,))

        if self.payload is None:
            raise Exception('no payload, please call load() first.')

        if self.storage is None:
            log.info('MemoryCard', 'save() no storage, NOOP')
            return

        await self.storage.save(self.payload)

    def _isMultiplexKey(self, key: str) -> bool:
        # if NAMESPACE_MULTIPLEX_SEPRATOR_REGEX.match(key) and NAMESPACE_KEY_SEPRATOR_REGEX.match(key):
        if re.search(NAMESPACE_MULTIPLEX_SEPRATOR_REGEX, key) and re.search(NAMESPACE_KEY_SEPRATOR_REGEX, key):
            namespace = self._multiplexNamespace()
            return key.startswith(namespace)

    def _multiplexNamespace(self) -> str:
        if not self.isMultiplex():
            raise Exception('not a multiplex memory')
        namespace = NAMESPACE_MULTIPLEX_SEPRATOR + NAMESPACE_MULTIPLEX_SEPRATOR.join(self.multiplexNameList)
        return namespace

    def _resolveKey(self, name: str) -> str:
        if self.isMultiplex():
            namespace = self._multiplexNamespace()
            return NAMESPACE_KEY_SEPRATOR.join([namespace, name])
        else:
            return name

    def isMultiplex(self) -> bool:
        return len(self.multiplexNameList) > 0

    def _multiplexPath(self) -> str:
        return '/'.join(self.multiplexNameList)

    def sub(self, name: str):
        log.warning('MemoryCard', 'sub() DEPRECATED, use multiplex() instead')
        return self.multiplex(name, memory=self)

    # FIXME Redeclared ?
    def multiplex_copy(self, name: str):
        log.info('MemoryCard', 'multiplex(%s)' % name)

        return self.multiplex(name=name, memory=self)

    async def destroy(self):
        log.info('MemoryCard', 'destroy() storage: %s' % self.storage)

        if self.isMultiplex():
            raise Exception('can not destroy on a multiplexed memory')

        await self.clear()

        if self.storage:
            await self.storage.destroy()
            self.storage = None

        self.payload = None

    @property
    def size(self) -> int:
        log.info('MemoryCard', '<%s> size' % self._multiplexPath())
        if self.payload is None:
            raise Exception('no payload, please call load() first.')
        # FIXME
        count: int = 0

        if self.isMultiplex():
            temp = filter(self._isMultiplexKey, self.payload.keys())
            for item in temp:
                if item:
                    count += 1
        else:
            count = len(self.payload.keys())
        return count

    async def get(self, name: str):
        log.info('MemoryCard', '<%s> get(%s)' % (self._multiplexPath(), name))

        if self.payload is None:
            raise Exception('no payload, please call load() first.')

        key = self._resolveKey(name)

        return self.payload.get(key)

    async def set(self, name, data):
        log.info('MemoryCard', '<%s> set(%s, %s)', self._multiplexPath(), name, data)

        if self.payload is None:
            raise Exception('no payload, please call load() first.')
        key = self._resolveKey(name)
        self.payload.update({key: data})

    async def entries(self):
        log.info('MemoryCard', '<%s> *entries()' % self._multiplexPath())
        if not self.payload:
            raise Exception('no payload, please call load() first.')

        # while True:
        #     try:
        #         relativeKey = next(self.keys())
        #         absoluteKey = self._resolveKey(relativeKey)
        #         data = self.payload[absoluteKey]
        #         pair = [relativeKey, data]
        #         yield pair
        #     except Exception as e:
        #         pass
        # pytype: disable=attribute-error
        for relativeKey in self.keys():
            absoluteKey = self._resolveKey(relativeKey)
            data = self.payload[absoluteKey]
            pair = [relativeKey, data]
            yield pair

    async def clear(self):
        log.info('MemoryCard', '<%s> clear()', self._multiplexPath())

        if self.payload is None:
            raise Exception('no payload, please call load() first.')

        if self.isMultiplex():
            for key in self.payload:
                if self._isMultiplexKey(key):
                    self.payload.pop(key)
        else:
            self.payload = {}

    async def delete(self, name: str):
        log.info('MemoryCard', '<%s> delete(%s)' % (self._multiplexPath(), name))

        if not self.payload:
            raise Exception('no payload, please call load() first.')
        key = self._resolveKey(name)
        self.payload.pop(key)

    async def has(self, key: str) -> bool:
        log.info('MemoryCard', '<%s> has(%s)' % (self._multiplexPath(), key))
        if not self.payload:
            raise Exception('no payload, please call load() first.')

        absoluteKey = self._resolveKey(key)
        return absoluteKey in self.payload

    async def keys(self):
        log.info('MemoryCard', '<%s> keys()' % self._multiplexPath())

        if not self.payload:
            raise Exception('no payload, please call load() first.')

        for key in self.payload.keys():
            if self.isMultiplex():
                if self._isMultiplexKey(key):
                    namespace = self._multiplexNamespace()
                    mpKey = key[(len(namespace) + 1):]
                    yield mpKey
                continue
            yield key

    async def values(self):
        log.info('MemoryCard', '<%s> values()' % self._multiplexPath())

        if not self.payload:
            raise Exception('no payload, please call load() first.')

        # while True:
        #     try:
        #         relativeKey = next(self.keys())
        #         absoluteKey = self._resolveKey(relativeKey)
        #         yield self.payload.get(absoluteKey)
        #     except Exception as e:
        #         pass
        # pytype: disable=attribute-error
        for relativeKey in self.keys():
            absoluteKey = self._resolveKey(relativeKey)
            yield self.payload.get(absoluteKey)
