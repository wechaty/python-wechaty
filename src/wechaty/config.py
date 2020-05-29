"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import re
from typing import (
    Optional,
)

from wechaty_puppet import (    # type: ignore
    FileBox,
    get_logger
)


log = get_logger('Config')

# log.debug('test logging debug')
# log.info('test logging info')


_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.realpath(
    os.path.join(
        _FILE_PATH,
        '../data',
    ),
)


def global_exception_handler(exception: Exception) -> None:
    """
    handle the global exception
    :param exception: exception message
    :return:
    """
    log.error('occur %s %s', exception.__class__.__name__, str(exception.args))
    print(exception)


class DefaultSetting(dict):
    """
    store global default setting
    """
    default_api_host: Optional[str] = None
    default_port: Optional[int] = None
    default_protocol: Optional[str] = None


# pylint: disable=R0903
def valid_api_host(api_host: str) -> bool:
    """
    test the validation of the api_host
    :param api_host:
    :return:
    """
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|:?[0-9]*'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|:?[0-9]*'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.:?[0-9]*'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3}):?[0-9]*$'
    )
    return bool(pattern.match(api_host))


class Config:
    """
    store python-wechaty configuration
    """
    # pylint: disable=R0913
    def __init__(self,
                 api_host: Optional[str] = None,
                 token: Optional[str] = None,
                 protocol: Optional[str] = None,
                 http_port: Optional[int] = None,
                 name: str = 'python-wechaty',
                 debug: bool = True,
                 docker: bool = False):
        """
        initialize the configuration
        """
        self.default = DefaultSetting

        self.api_host = api_host if api_host is not None \
            else DefaultSetting.default_api_host

        self.http_port = http_port if http_port is not None \
            else DefaultSetting.default_port

        self.protocol = protocol if protocol is not None \
            else DefaultSetting.default_protocol

        if token is None:
            raise AttributeError('token can"t be None')

        self.name = name
        self.debug = debug
        self.docker = docker

        if self.api_host is not None and not valid_api_host(self.api_host):
            raise AttributeError('api host %s is not valid' % self.api_host)


# export const CHATIE_OFFICIAL_ACCOUNT_ID = 'gh_051c89260e5d'
# chatie_official_account_id = 'gh_051c89260e5d'
# CHATIE_OFFICIAL_ACCOUNT_ID = 'gh_051c89260e5d'


def qr_code_for_chatie() -> FileBox:
    """
    create QRcode for chatie
    :return:
    """
    # const CHATIE_OFFICIAL_ACCOUNT_QRCODE =
    # 'http://weixin.qq.com/r/qymXj7DEO_1ErfTs93y5'
    chatie_official_account_qr_code: str = \
        'http://weixin.qq.com/r/qymXj7DEO_1ErfTs93y5'
    return FileBox.from_qr_code(chatie_official_account_qr_code)
