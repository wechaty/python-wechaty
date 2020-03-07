"""
accessory unit test
"""
from typing import (
    cast,
    Type,
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


def get_child_class():
    """create a fixture"""

    class FixtureClass(Accessory):
        """fixture"""

    return FixtureClass


@pytest.fixture(name='user_class')
def fixture_user_class():
    """fixture for fixture class"""
    yield get_child_class()


def test_indenpendent_child_classes():
    """two child class should not be equal"""
    child_class1 = get_child_class()
    child_class2 = get_child_class()

    assert child_class1 != child_class2, 'two child class should not be equal'


def test_child_classes_should_share():
    """doc"""

    child_class = get_child_class()

    child_class.wechaty = EXPECTED_WECHATY1
    child_class.puppet  = EXPECTED_PUPPET1

    child1 = child_class()
    child2 = child_class()

    assert child1.wechaty == EXPECTED_WECHATY1, \
        'child1 should get the wechaty from static value'
    assert child2.wechaty == EXPECTED_WECHATY1, \
        'child1 should get the wechaty from static value'


def test_indenpendent_chlid_classes_instances():
    """doc"""

    child_class1 = get_child_class()
    child_class2 = get_child_class()

    child_class1.wechaty = EXPECTED_WECHATY1
    child_class1.puppet = EXPECTED_PUPPET1

    child_class2.wechaty = EXPECTED_WECHATY2
    child_class2.puppet = EXPECTED_PUPPET2

    child_class1_instance = child_class1()
    child_class2_instance = child_class2()

    assert child_class1_instance.wechaty == EXPECTED_WECHATY1, \
        'class1 instance should get wechaty1'
    assert child_class1_instance.puppet == EXPECTED_PUPPET1, \
        'class1 instance should get puppet1'

    assert child_class2_instance.wechaty == EXPECTED_WECHATY2, \
        'class2 instance should get wechaty2'
    assert child_class2_instance.puppet == EXPECTED_PUPPET2, \
        'class2 instance should get puppet2'


def test_accessory_read_uninitialized_static(
        user_class: Type[Accessory],
):
    """should throw if read static wechaty & puppet before initialization"""

    with pytest.raises(Exception) as e:
        assert user_class.puppet
    assert str(e.value) == 'static puppet not found ...'

    with pytest.raises(Exception) as e:
        assert user_class.wechaty
    assert str(e.value) == 'static wechaty not found ...'


def test_accessory_read_initialized_class(
        user_class: Type[Accessory],
):
    """
    should read excepted value by reading static wechaty & puppet after init
    """

    # reveal_type(accessory_class.wechaty)

    user_class.puppet  = EXPECTED_PUPPET1
    user_class.wechaty = EXPECTED_WECHATY1

    assert \
        user_class.puppet == EXPECTED_PUPPET1, \
        'should get puppet back'
    assert \
        user_class.wechaty == EXPECTED_WECHATY1, \
        'should get wechaty back'

    accessory_instance = user_class()

    assert \
        accessory_instance.puppet == EXPECTED_PUPPET1, \
        'should get puppet back by instance from static'
    assert \
        accessory_instance.wechaty == EXPECTED_WECHATY1, \
        'should get wechaty back by instance from static'


def test_accessory_read_uninitialized_instance(
        user_class: Type[Accessory],
):
    """should throw if read instance wechaty & puppet before initialization"""
    # pytest.skip('tbd')

    instance = user_class()

    with pytest.raises(Exception) as e:
        assert instance.puppet
    assert str(e.value) == 'static puppet not found ...'

    with pytest.raises(Exception) as e:
        assert instance.wechaty
    assert str(e.value) == 'static wechaty not found ...'


def test_accessory_read_initialized_instance(
        user_class: Type[Accessory],
):
    """
    should get expected value by reading instance wechaty & puppet after init
    """

    user_class.puppet  = EXPECTED_PUPPET1
    user_class.wechaty = EXPECTED_WECHATY1

    # reveal_type(accessory_class)
    accessory_instance = user_class()

    assert \
        accessory_instance.puppet == EXPECTED_PUPPET1, \
        'should get puppet back'
    assert \
        accessory_instance.wechaty == EXPECTED_WECHATY1, \
        'should get wechaty back'


def test_accessory_isolate_static_value():
    """
    doc
    """

    class Fixture1(Accessory):
        """Fixture1"""

    class Fixture2(Accessory):
        """Fixture2"""

    Fixture1.puppet  = EXPECTED_PUPPET1
    Fixture1.wechaty = EXPECTED_WECHATY1

    Fixture2.puppet  = EXPECTED_PUPPET2
    Fixture2.wechaty = EXPECTED_WECHATY2

    assert Fixture1.puppet  != Fixture2.puppet,  \
        'should isolate the static puppet value'
    assert Fixture1.wechaty != Fixture2.wechaty, \
        'should isolate the static wechaty value'

    instance1 = Fixture1()
    instance2 = Fixture2()

    assert instance1.puppet  != instance2.puppet, \
        'should isolate the instance puppet value'
    assert instance1.wechaty != instance2.wechaty, \
        'should isolate the instance wechaty value'


# TODO: add set twice exception test
