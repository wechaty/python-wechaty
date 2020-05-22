from __future__ import annotations
from .backend_config import (
    BACKEND_DICT,
    StorageBackendOptions,
    StorageFileOptionsExtends
)
from typing import Optional
from .backend import StorageBackend

import logging

log = logging.getLogger('getStorage')


def getStorage(name: Optional[str] = None, options: StorageBackendOptions = None) -> StorageBackend:

    if options is None:
        options = StorageFileOptionsExtends(type='file')

    if not name:
        print("options", options)
        if not options.type == 'nop':
            raise Exception('storage have to be `nop` with a un-named storage')
        name = 'nop'

    if (not options.type) or (not (options.type in BACKEND_DICT)):
        raise Exception('backend unknown: ' + options.type)

    Backend = BACKEND_DICT[options.type]
    backend = Backend(name, options)
    return backend
