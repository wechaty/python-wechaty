"""doc"""
from __future__ import annotations
from os import path
import logging
import json
import re
from typing import (
    Optional,
    List,
    Union
)

from dataclasses import dataclass

from .config import VERSION
from .storage import (
    getStorage,
    StorageBackend,
    StorageBackendOptions
)
from .types import (
    AsyncMap,
    MemoryCardPayload
)
import collections
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
    name: Optional[str]
    storageOptions: Optional[StorageBackendOptions]
    multiplex: Optional = None


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

    name: Optional[str] = None

    parent: Optional[MemoryCard] = None
    payload: Optional[MemoryCardPayload] = None
    storage: Optional[StorageBackend] = None
    multiplexNameList: List[str]

    options: Optional[MemoryCardOptions] = None

    def __init__(self, options: Optional[Union[str, MemoryCardOptions]]):
        super().__init__()
        log.info('MemoryCard', 'constructor(%s)' % json.dumps(options))

        if type(options) == str:
            options = {self.name, options}

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
            self.storage = self._getStorage()

    def toString(self):
        pass

    @property
    def version(self) -> str:
        return VERSION

    def _getStorage(self):
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

        log.info('MemoryCard', '<%s>%s save() to %s' % (self.name and '', self.multiplexPath(), self.storage and None,))

        if not self.payload:
            raise Exception('no payload, please call load() first.')

        if not self.storage:
            log.info('MemoryCard', 'save() no storage, NOOP')
            return

        await self.storage.save(self.payload)

    def isMultiplexKey(self, key: str) -> bool:
        if NAMESPACE_MULTIPLEX_SEPRATOR_REGEX.match(key) and NAMESPACE_KEY_SEPRATOR_REGEX.match(key):
            namespace = self.multiplexNamespace()
            return key.startswith(namespace)

    def multiplexNamespace(self) -> str:
        if not self.isMultiplex():
            raise Exception('not a multiplex memory')
        namespace = NAMESPACE_MULTIPLEX_SEPRATOR + NAMESPACE_MULTIPLEX_SEPRATOR.join(self.multiplexNameList)
        return namespace

    def resolveKey(self, name: str) -> str:
        if self.isMultiplex():
            namespace = self.multiplexNamespace()
            return NAMESPACE_KEY_SEPRATOR.join([namespace, name])
        else:
            return name

    @classmethod
    def isMultiplex(cls) -> bool:
        return len(cls.multiplexNameList) > 0

    @classmethod
    def multiplexPath(cls) -> str:
        return '/'.join(cls.multiplexNameList)

    def sub(self, name: str):
        log.warning('MemoryCard', 'sub() DEPRECATED, use multiplex() instead')
        return self.multiplex(name)

    def multiplex(self, name: str):
        log.info('MemoryCard', 'multiplex(%s)' % name)

        # FIXME: as any ?
        return self.multiplex(name)

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
        log.info('MemoryCard', '<%s> size' % self.multiplexPath())
        if not self.payload:
            raise Exception('no payload, please call load() first.')
        # FIXME
        count: int = -1
        if self.isMultiplex():
            # TODO
            pass
        else:
            # TODO
            count = len(self.keys())
        return count

    async def get(self, name: str):
        log.info('MemoryCard', '<%s> get(%s)' % (self.multiplexPath(), name))

        if not self.payload:
            raise Exception('no payload, please call load() first.')

        key = self.resolveKey(name)

    async def set(self, name, data):
        log.info('MemoryCard', '<%s> set(%s, %s)', self.multiplexPath(), name, data)

        if not self.payload:
            raise Exception('no payload, please call load() first.')

        key = self.resolveKey(name)
        self.payload.key = data

    async def clear(self):
        log.info('MemoryCard', '<%s> clear()', self.multiplexPath())

        if not self.payload:
            raise Exception('no payload, please call load() first.')

        if self.isMultiplex():
            for key in self.payload:
                if self.isMultiplexKey(key):
                    del self.payload.key
        else:
            self.payload = {}

    async def delete(self, name: str):
        log.info('MemoryCard', '<%s> delete(%s)' % (self.multiplexPath(), name))

        if not self.payload:
            raise Exception('no payload, please call load() first.')
        key = self.resolveKey(name)
        del self.payload.key

    async def has(self, key: str) -> bool:
        log.info('MemoryCard', '<%s> has(%s)' % (self.multiplexPath(), key))
        if not self.payload:
            raise Exception('no payload, please call load() first.')

        absoluteKey = self.resolveKey(key)
        return absoluteKey in self.payload
