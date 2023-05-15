"""
Unit test
"""
import pytest
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from wechaty_puppet import WechatyPuppetConfigurationError
from wechaty import Wechaty, WechatyOptions 

def test_constructor():
    # remove environment variables
    os.environ.pop("token", None)
    os.environ.pop("WECHATY_TOKEN", None)
    
    with pytest.raises(WechatyPuppetConfigurationError):
        bot = Wechaty()

    options = WechatyOptions(token='fake-token', endpoint='127.0.0.1:8080')
    bot = Wechaty(options=options)
    
    assert bot.puppet.options.token == 'fake-token'
    assert bot.puppet.options.end_point == '127.0.0.1:8080'


def test_scheduler():
    """test add scheduler in the options"""
    scheduler = AsyncIOScheduler()
    options = WechatyOptions(
        scheduler=scheduler
    )
    bot = Wechaty(options=options)
    assert id(scheduler) == id(bot._plugin_manager.scheduler)
