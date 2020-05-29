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
from __future__ import annotations

from wechaty_puppet import MiniProgramPayload, get_logger   # type: ignore


log = get_logger('MiniProgram')


class MiniProgram:
    """
    mini_program object which handle the url_link content
    """
    def __init__(self, payload: MiniProgramPayload):
        """
        initialization for mini_program
        :param payload:
        """
        log.info('MiniProgram created')
        self.payload: MiniProgramPayload = payload

    @classmethod
    async def create(cls) -> MiniProgram:
        """
        static create MiniProgram method
        :return:
        """
        log.info('MiniProgram created')
        # TODO -> create default mini_program payload
        payload = MiniProgramPayload()
        return MiniProgram(payload)

    @property
    def app_id(self) -> str:
        """
        get mini_program app_id
        :return:
        """
        if self.payload.app_id is None:
            return ''
        return self.payload.app_id

    @property
    def title(self) -> str:
        """
        get mini_program title
        :return:
        """
        if self.payload.title is None:
            return ''
        return self.payload.title

    @property
    def page_path(self) -> str:
        """
        get mini_program page_path
        :return:
        """
        if self.payload.page_path is None:
            return ''
        return self.payload.page_path

    @property
    def user_name(self) -> str:
        """
        get mini_program user_name
        :return:
        """
        if self.payload.user_name is None:
            return ''
        return self.payload.user_name

    @property
    def description(self) -> str:
        """
        get mini_program description
        :return:
        """
        if self.payload.description is None:
            return ''
        return self.payload.description

    @property
    def thumb_url(self) -> str:
        """
        get mini_program thumb_url
        :return:
        """
        if self.payload.thumb_url is None:
            return ''
        return self.payload.thumb_url

    @property
    def thumb_key(self) -> str:
        """
        get mini_program thumb_key
        :return:
        """
        if self.payload.thumb_key is None:
            return ''
        return self.payload.thumb_key
