"""unittest for plugin"""
import json
import os
import tempfile
import unittest
from wechaty import Wechaty, WechatyOptions
from wechaty.plugin import WechatyPlugin
from wechaty.utils.data_util import WechatySetting
from wechaty.fake_puppet import FakePuppet


def test_setting():
    with tempfile.TemporaryDirectory() as cache_dir:
        os.environ['CACHE_DIR'] = cache_dir
        plugin = WechatyPlugin()
        
        plugin.setting['unk'] = 11

        assert 'count' not in plugin.setting
        plugin.setting['count'] = 20

        # load the setting file
        assert os.path.exists(plugin.setting_file)

        with open(plugin.setting_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data['unk'] == 11
        assert data['count'] == 20


class TestWechatySetting(unittest.TestCase):

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
    
    def tearDown(self) -> None:
        self.tempdir.cleanup()

    
    def test_simple_init(self):
        setting_file = os.path.join(self.tempdir.name, 'simple_setting.json')
        wechaty_setting: WechatySetting = WechatySetting(setting_file)

        assert os.path.exists(setting_file)

        wechaty_setting['a'] = 'a'
        assert 'a' in wechaty_setting.read_setting()
        assert wechaty_setting.read_setting()['a'] == 'a'
        
        assert 'b' not in wechaty_setting

        assert wechaty_setting.get("b", "b") == "b"
        
        wechaty_setting.save_setting({"c": "c"})
        assert 'a' not in wechaty_setting
        assert 'c' in wechaty_setting
    
    def test_sub_setting(self):
        setting_file = os.path.join(self.tempdir.name, "sub", 'simple_setting.json')
        wechaty_setting: WechatySetting = WechatySetting(setting_file)

        assert os.path.exists(setting_file)

        wechaty_setting['a'] = 'a'
        assert 'a' in wechaty_setting.read_setting()
        assert wechaty_setting.read_setting()['a'] == 'a'
        
        assert 'b' not in wechaty_setting

        assert wechaty_setting.get("b", "b") == "b"
        
        wechaty_setting.save_setting({"c": "c"})
        assert 'a' not in wechaty_setting
        assert 'c' in wechaty_setting


    async def test_finder(self):
        fake_puppet = FakePuppet()
        bot = Wechaty(options=WechatyOptions(puppet=fake_puppet))

        contact_id = fake_puppet.add_random_fake_contact()

        contact_payload = await fake_puppet.contact_payload(contact_id)
        from wechaty_plugin_contrib.finders.contact_finder import ContactFinder
        finder = ContactFinder(
            contact_id
        )
        contacts = await finder.match(bot)
        assert len(contacts) == 1
        
        contact = contacts[0]
        await contact.ready()
        
        assert contact.payload.name == contact_payload.name
        