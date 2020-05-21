from ..types import MemoryCardPayload
from .backend import StorageBackend
from .backend_config import (
    StorageBackendOptions,
    StorageObsOptions
)

import logging
log = logging.getLogger('obs')

# TODO ObsClient


class StorageObs(StorageBackend):
    obs = None

    def __init__(self, name: str, options: StorageBackendOptions):
        log.info('StorageObs', 'constructor()')
        options.type = 'obs'
        super().__init__(name, options)
        # TODO ObsClient

    def toString(self) -> str:
        text = ''.join([self.name, '<', self.name, '>'])
        return text

    async def save(self, payload: MemoryCardPayload) -> None:
        log.info('StorageObs', 'save()')
        # TODO

    async def load(self) -> MemoryCardPayload:
        log.info('StorageObs', 'load()')
        return {}

    async def destroy(self) -> None:
        log.info('StorageObs', 'destroy()')
        await self.deleteObject()

    async def putObject(self, payload: MemoryCardPayload) -> None:
        # TODO
        pass

    async def getObject(self) -> None:
        # TODO
        pass

    async def deleteObject(self) -> None:
        # TODO
        pass

