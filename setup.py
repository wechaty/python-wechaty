"""
setup
"""
import os

import semver
import setuptools


def versioning(version: str) -> str:
    """
    version to specification
    Author: Huan <zixia@zixia.net> (https://github.com/huan)

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


def get_version() -> str:
    """
    read version from VERSION file
    """
    version = '0.0.0'

    with open(
            os.path.join(
                os.path.dirname(__file__),
                'VERSION'
            )
    ) as version_fh:
        # Get X.Y.Z
        version = version_fh.read().strip()
        # versioning from X.Y.Z to X.Y.devZ
        version = versioning(version)

    return version


with open('README.md', 'r') as readme_fh:
    long_description = readme_fh.read()

setuptools.setup(
    name='wechaty',
    version=get_version(),
    author='Huan LI (李卓桓)',
    author_email='zixia@zixia.net',
    description='Wechaty is a Bot SDK for Wechat Personal Account',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    url='https://github.com/wechaty/python-wechaty',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['pyee', 'requests', 'qrcode', 'wechaty-puppet'],
    # packages=setuptools.find_packages('wip'),
    # package_dir={'': 'wip'},
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
