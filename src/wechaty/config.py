'''
config module
'''
import logging
import os

logging.basicConfig(
    filename="logging.log",
    level=logging.DEBUG,
)

log = logging.getLogger('Wechaty')

# log.debug('test logging debug')
# log.info('test logging info')

_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.realpath(
    os.path.join(
        _FILE_PATH,
        '../data',
    ),
)
