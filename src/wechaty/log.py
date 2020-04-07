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

import logging
from functools import wraps
from inspect import isfunction


class WechatyLogger:
    """
    WechatyLogger decorator
    """

    def __init__(self, module_name: str = None, log_level: int = 20):
        """
        default log module_name is Wechaty
        default log_level is logging.INFO
        """
        module_name = 'Wechaty' if module_name is None else module_name
        self.logger = logging.getLogger(module_name)
        self.log_level = log_level

    def __call__(self, *args, **kwargs):
        """
        decorator caller
        example code:

        logger = WechatyLogger()

        @logger
        @logger()
        def method():
            # do something

        @logger(logging.INFO)
        @logger(level=logging.INFO)
        def method():
            # do something
        """
        if len(kwargs) == 0 and len(args) == 1 and isfunction(args[0]):
            @wraps(args[0])
            def wrapper(*func_args, **func_kwargs):
                self._execute(args[0], *func_args, **func_kwargs)

            return wrapper
        if len(kwargs) != 0 or len(args) == 0 or not isfunction(args[0]):
            # parse log_level in params
            if 'level' in kwargs and isinstance(kwargs['level'], int):
                log_level = kwargs['level']
            elif len(args) > 0 and isinstance(args[0], int):
                log_level = args[0]
            else:
                log_level = None

            def decorator(func):
                @wraps(func)
                def decorator_wrapper(*func_args, **func_kwargs):
                    self._execute(func, log_level, *func_args, **func_kwargs)
                return decorator_wrapper
            return decorator

        raise Exception('params not valida')

    def _execute(self, func, log_level, *args, **kwargs):
        level = self.log_level if log_level is None else log_level
        self.logger.setLevel(level)
        # log debug information show in only when user set logging.DEBUG
        func_name = func.__name__
        # pylint: disable=W0511
        # todo -> need to add more beautiful of debug params message format
        # debug_msg_format = f"%s() params: <%s> kwargs: "
        self.logger.debug('%s() <%s> <%s>', func_name, *args, **kwargs)
        self._log_by_level(level, func_name, *args, **kwargs)
        result = func(*args, **kwargs)
        self.logger.debug('%s() return value: <%s>', func_name, result)
        return result

    def _log_by_level(self, log_level: int, func_name: str, *args, **kwargs):
        """
        because log_level is a integer data type, we need to switch to log

        logger level is
        CRITICAL = 50
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
        """
        logger_func_map = {
            50: 'fatal',
            40: 'error',
            30: 'warning',
            20: 'info',
            10: 'debug'
        }
        if log_level not in logger_func_map:
            raise Exception('logger level is a wrong value')
        if not hasattr(self.logger, logger_func_map[log_level]):
            raise Exception('logger instance is not a python logging logger')
        logger_func = getattr(self.logger, logger_func_map[log_level])
        logger_func('%s() <%s> <%s>', func_name, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """
        wrap the logging info method
        """
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        """
        wrap the logging debug method
        """
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """
        wrap the logging debug method
        """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """
        wrap the logging debug method
        """
        self.logger.error(msg, *args, **kwargs)

    def fatal(self, msg: str, *args, **kwargs):
        """
        wrap the logging debug method
        """
        self.logger.fatal(msg, *args, **kwargs)
