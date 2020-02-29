''' setup '''

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

version = '0.0.0'
with open('VERSION', 'r') as fh:
    version = fh.readline()

setuptools.setup(
    name='wechaty',
    version=version,
    author='Huan LI (李卓桓)',
    author_email='zixia@zixia.net',
    description='Wechaty is a Bot SDK for Wechat Personal Account',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Chatie/python-wechaty',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
