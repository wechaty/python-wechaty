"""TODO doc"""
# from boto3
from ..types import MemoryCardPayload
from .backend import StorageBackend
from .backend_config import (
    StorageBackendOptions,
    StorageS3Options
)
import logging
log = logging.getLogger('S3')


class StorageS3(StorageBackend):
    s3: S3

    def __init__(self, name: str, options: StorageBackendOptions):
        log.info('StorageS3', 'constructor()')
        options.type = 's3'
        super().__init__(name, options)

        self.s3 = S3
