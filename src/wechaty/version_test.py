"""
version unit test
"""
# import pytest   # type: ignore

from .version import VERSION
import os


def test_version() -> None:
    """
    Unit Test for version file
    """
    version_file = os.path.join(os.getcwd(), 'VERSION')
    if not os.path.exists(version_file):
        raise FileNotFoundError('VERSION file not found')
    with open(version_file, 'r') as f:
        version = f.read().strip()

    assert VERSION == version, 'version should be consist with VERSION file'
