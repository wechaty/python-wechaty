'''
config module
'''
import logging
import os


# dummy class
class FileBox:
    '''FileBox'''

    def toJSON(self):
        '''doc'''

    def toFile(self):
        '''doc'''


log = logging.getLogger(__name__)

# log.debug('test logging debug')
# log.info('test logging info')

_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.realpath(
    os.path.join(
        _FILE_PATH,
        '../data',
    ),
)
