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

import asyncio
from asyncio import coroutine
from collections import Callable
import logging
from typing import Optional, Any

from pyee import AsyncIOEventEmitter
from datetime import datetime
from dataclasses import dataclass

log = logging.getLogger("Watchdog")


@dataclass
class WatchdogFood:
    timeout: float
    type: Optional[Any] = None


class Watchdog(AsyncIOEventEmitter):
    """
    watch dog based on asyncio coroutine
    """
    def __init__(self, default_timeout: int = 30, name: str = 'Bark'):
        """
        init the watch dog
        """
        super(Watchdog, self).__init__()
        self._last_feed: Optional[datetime] = None
        self._last_food: Optional[WatchdogFood] = None
        self.default_timeout: int = default_timeout
        self.name = name
        self.timer = None

    def on(self, event, f=None) -> Watchdog:
        """listen for the watchdog event"""
        log.info('watchdog <%s> <%s> registered', event, f)
        super().on(event, f)
        return self

    def _start_timer(self, timeout: int):
        """start the timer to record watchdog"""
        log.info('Watchdog <%s> _start_timer() setTimeout() after %d',
                 self.name, timeout)

        if self.timer is not None:
            raise ValueError('timer already exist !')

        asyncio.sleep(timeout)
        timeout = self._last_food.timeout if self._last_food is not None else \
            self.default_timeout
        self.emit('reset', self._last_food, timeout)

    def feed(self, food: WatchdogFood):
        """feed the food to the watch dog"""
        log.info('feed the food <%s> the watchdog', food)
        self._last_food = food
        self._last_feed = datetime.now()
        self.emit('feed', food, self._last_feed)

    async def sleep(self) -> bool:
        """dog can sleep"""
        if self._last_food is not None and self._last_feed is not None:
            await asyncio.sleep(self._last_food.timeout)
            timeout = (datetime.now() - self._last_feed).seconds
            if timeout > self.default_timeout:
                self.emit('reset', self._last_food, self._last_feed)
                return False
            else:
                self.emit('sleep')
        return True


async def main():
    """example code of the watchdog"""
    def dog_food() -> bool:
        print("can get the food")
        return True

    food = WatchdogFood(data=dog_food, timeout=1)
    dog = Watchdog(3)

    def reset(food, time):
        print('reset the dog')

    dog.on('reset', reset)
    dog.feed(food)
    while True:
        has_no_food = await dog.sleep()
        print("eating food ...")
        if has_no_food:
            break
    print("all done ...")

# asyncio.run(main())
