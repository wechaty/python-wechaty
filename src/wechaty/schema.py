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
from enum import Enum
import os
from typing import Any, Optional, List, Dict, Union
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from quart import jsonify, Response
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from wechaty.config import config


@dataclass_json
@dataclass
class NavMetadata:
    """nav metadata"""
    view_url: Optional[str] = None
    author: Optional[str] = None    # name of author
    avatar: Optional[str] = None    # avatar of author
    author_link: Optional[str] = None    # introduction link of author
    icon: Optional[str] = None    # avatar of author


@dataclass_json
@dataclass
class NavDTO:
    """the data transfer object of plugin list"""
    name: str                       # name of plugin
    status: int                     # status of plugin: 0 / 1

    view_url: Optional[str] = None
    author: Optional[str] = None    # name of author
    avatar: Optional[str] = None    # avatar of author
    author_link: Optional[str] = None    # introduction link of author
    icon: Optional[str] = None    # avatar of author

    def update_metadata(self, nav_metadata: NavMetadata) -> None:
        """update the field with nav data
        """
        self.author = nav_metadata.author
        self.author_link = nav_metadata.author_link
        self.avatar = nav_metadata.avatar
        self.icon = nav_metadata.icon
        self.view_url = nav_metadata.view_url


def success(data: Any) -> Response:
    """make the success response with data

    Args:
        data (dict): the data of response
    """
    return jsonify(dict(
        code=200,
        data=data
    ))


def error(msg: str) -> Response:
    """make the error response with msg

    Args:
        msg (str): the error msg string of data
    """
    return jsonify(dict(
        code=500,
        msg=msg
    ))


@dataclass
class WechatyPluginOptions:
    """options for wechaty plugin"""
    name: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class WechatySchedulerOptions:
    """options for wechaty scheduler"""
    job_store: Union[str, SQLAlchemyJobStore] = f'sqlite:///{config.cache_dir}/job.db'
    job_store_alias: str = 'wechaty-scheduler'


class PluginStatus(Enum):
    """plugin running status"""
    Running = 0
    Stopped = 1


class StaticFileCacher:
    """cache the static file to avoid time-consuming finding and loading
    """
    def __init__(self, cache_dirs: Optional[List[str]] = None) -> None:
        self.file_maps: Dict[str, str] = {}

        self.cache_dirs = cache_dirs or []

    def add_dir(self, static_file_dir: Optional[str]) -> None:
        """add the static file dir

        Args:
            static_file_dir (str): the path of the static file
        """
        if not static_file_dir:
            return
        self.cache_dirs.append(static_file_dir)

    def _find_file_path_recursive(self, base_dir: str, name: str) -> Optional[str]:
        """find the file based on the file-name which will & should be union

        Args:
            base_dir (str): the root dir of static files for the plugin
            name (str): the union name of static file

        Returns:
            Optional[str]: the target static file path
        """
        if not os.path.exists(base_dir) or os.path.isfile(base_dir):
            return None

        for file_name in os.listdir(base_dir):
            if file_name == name:
                return os.path.join(base_dir, file_name)
            file_path = os.path.join(base_dir, file_name)

            target_path = self._find_file_path_recursive(file_path, name)
            if target_path:
                return target_path

        return None

    def find_file_path(self, name: str) -> Optional[str]:
        """find the file based on the file-name which will & should be union

        Args:
            name (str): the union name of static file

        Returns:
            Optional[str]: the path of the static file
        """
        if name in self.file_maps:
            return self.file_maps[name]

        for cache_dir in self.cache_dirs:
            file_path = self._find_file_path_recursive(cache_dir, name)
            if file_path:
                return file_path
        return None
