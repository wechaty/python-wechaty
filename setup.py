"""
setup
"""
import os

import semver
import setuptools


def versioning(version: str) -> str:
    """
    version to specification

    X.Y.Z -> X.Y.devZ

    """
    sem_ver = semver.parse(version)

    major = sem_ver['major']
    minor = sem_ver['minor']
    patch = str(sem_ver['patch'])

    if minor % 2:
        patch = 'dev' + patch

    fin_ver = '%d.%d.%s' % (
        major,
        minor,
        patch,
    )

    return fin_ver


def setup() -> None:
    """setup"""

    with open('README.md', 'r') as fh:
        long_description = fh.read()

    __version__ = '0.0.0'
    with open(
            os.path.join(
                os.path.dirname(__file__),
                'VERSION'
            )
    ) as fh:
        # Get X.Y.Z
        __version__ = fh.read().strip()
        # versioning from X.Y.Z to X.Y.devZ
        __version__ = versioning(__version__)

    setuptools.setup(
        name='wechaty',
        version=__version__,
        author='Huan LI (李卓桓)',
        author_email='zixia@zixia.net',
        description='Wechaty is a Bot SDK for Wechat Personal Account',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='Apache-2.0',
        url='https://github.com/wechaty/python-wechaty',
        # packages=setuptools.find_packages('src'),
        # package_dir={'': 'src'},
        packages=setuptools.find_packages('wip'),
        package_dir={'': 'wip'},
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
        ],
    )


setup()
