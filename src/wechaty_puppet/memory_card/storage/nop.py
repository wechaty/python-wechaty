from __future__ import annotations
from ..types import MemoryCardPayload
from .backend import StorageBackend
from .backend_config import StorageBackendOptions

import logging

log = logging.getLogger('nop')


class StorageNop(StorageBackend):

    def __init__(self, name: str, options: StorageBackendOptions):
        log.info('StorageNop', 'constructor(%s, ...)' % name)
        super().__init__(name, options)

    def toString(self) -> str:
        text = ''.join([self.name, '<nop>'])
        return text

    async def load(self) -> MemoryCardPayload:
        log.info('StorageNop', 'load()')
        return {}

    async def save(self, _: MemoryCardPayload) -> None:
        log.info('StorageNop', 'save()')

    async def destroy(self) -> None:
        log.info('StorageNop', 'destroy()')
