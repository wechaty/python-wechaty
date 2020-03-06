"""
accessory unit test
"""
from typing import (
    cast,
)
import pytest   # type: ignore

from wechaty import (
    Wechaty,
)
from wechaty_puppet import (
    Puppet,
)
from .accessory import (
    Accessory,
)

EXPECTED_PUPPET1 = cast(Puppet, {'p': 1})
EXPECTED_PUPPET2 = cast(Puppet, {'p': 2})

EXPECTED_WECHATY1 = cast(Wechaty, {'w': 1})
EXPECTED_WECHATY2 = cast(Wechaty, {'w': 1})


def test_accessory_read_uninitialized_static_wechaty_puppet(
        accessory_class: Accessory,
):
    """should throw if read static wechaty & puppet before initialization"""

    with pytest.raises(Exception) as e:
        assert accessory_class.puppet
    assert str(e.value) == 'static puppet not found ...'

    with pytest.raises(Exception) as e:
        assert accessory_class.wechaty
    assert str(e.value) == 'static wechaty not found ...'


def test_accessory_read_initialized_class_wechaty_puppet(
        accessory_class: Accessory,
):
    """
    should read excepted value by reading static wechaty & puppet after init
    """

    accessory_class.puppet  = EXPECTED_PUPPET1
    accessory_class.wechaty = EXPECTED_WECHATY1

    assert \
        accessory_class.puppet == EXPECTED_PUPPET1, \
        'should get puppet back'
    assert \
        accessory_class.wechaty == EXPECTED_WECHATY1, \
        'should get wechaty back'

    accessory_instance = accessory_class()

    assert \
        accessory_instance.puppet == EXPECTED_PUPPET1, \
        'should get puppet back by instance from static'
    assert \
        accessory_instance.wechaty == EXPECTED_WECHATY1, \
        'should get wechaty back by instance from static'


def test_accessory_read_uninitialized_instance_wechaty_puppet(
        accessory_class,
):
    """should throw if read instance wechaty & puppet before initialization"""
    # pytest.skip('tbd')

    instance = accessory_class()

    with pytest.raises(Exception) as e:
        print(instance.puppet)
        assert instance.puppet
    assert str(e.value) == 'static puppet not found ...'

    with pytest.raises(Exception) as e:
        assert instance.wechaty
    assert str(e.value) == 'static wechaty not found ...'


def test_accessory_read_initialized_instance_wechaty_puppet(
        accessory_class: Accessory,
):
    """
    should get expected value by reading instance wechaty & puppet after init
    """

    accessory_instance = accessory_class()

    accessory_instance.puppet  = EXPECTED_PUPPET1
    accessory_instance.wechaty = EXPECTED_WECHATY1

    assert \
        accessory_instance.puppet == EXPECTED_PUPPET1, \
        'should get puppet back'
    assert \
        accessory_instance.wechaty == EXPECTED_WECHATY1, \
        'should get wechaty back'


@pytest.fixture(name='accessory_class')
def fixture_accessory_class():
    """create a fixture"""

    class FixtureClass(Accessory):
        """fixture"""

    yield FixtureClass
