"""unittest for plugin"""
import json
import os
import tempfile
from wechaty.plugin import WechatyPlugin


def test_setting():
    with tempfile.TemporaryDirectory() as cache_dir:
        os.environ['CACHE_DIR'] = cache_dir
        plugin = WechatyPlugin()
        
        plugin.setting['unk'] = 11
        plugin.setting['count'] += 20

        # load the setting file
        assert os.path.exists(plugin.setting_file)

        with open(plugin.setting_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data['unk'] == 11
        assert data['count'] == 20

