from __future__ import annotations
from .backend_config import (
    BACKEND_DICT,
    StorageBackendOptions
)
from typing import Optional
from .backend import StorageBackend

import logging
import json

log = logging.getLogger('getStorage')


# options : StorageBackendOptions = {type: 'file'}
def getStorage(name: Optional[str] = None, options: StorageBackendOptions = None) -> StorageBackend:

    if options is None:
        options = {type: 'file'}

    log.info('getStorage', 'name: %s, options: %s' % (name, json.dumps(options)))
    if not name:
        if not options.type == 'nop':
            raise Exception('storage have to be `nop` with a un-named storage')
        name = 'nop'

    if (not options.type) or (not (options.type in BACKEND_DICT)):
        raise Exception('backend unknown: ' + options.type)

    Backend = BACKEND_DICT[options.type]
    backend = Backend(name, options)
    return backend
