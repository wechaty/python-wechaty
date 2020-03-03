"""
 *
 *   Wechaty - https://github.com/wechaty/python-wechaty
 *
 *   @copyright wechaty
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 *
 """
import logging
import os

LOG = logging.getLogger(__name__)

# log.debug('test logging debug')
# log.info('test logging info')

_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.realpath(
    os.path.join(
        _FILE_PATH,
        '../data',
    ),
)
