"""doc"""
from __future__ import annotations
import logging
from wechaty_puppet.memory_card.types import MemoryCardPayload
from .backend_config import StorageBackendOptions

log = logging.getLogger("backend")


class StorageBackend:

    def __init__(self, name: str, options: StorageBackendOptions):
        log.info('StorageBackend', 'constructor(%s, { type: %s })' % (name, options.type))
        self.name = name
        self.options = options

    def save(self, payload: MemoryCardPayload):
        raise NotImplementedError

    def load(self) -> MemoryCardPayload:
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError
