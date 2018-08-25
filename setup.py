""" setup """

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wechaty",
    version="0.0.2",
    author="Huan LI",
    author_email="zixia@zixia.net",
    description="Wechaty is a Bot SDK for Wechat Personal Account",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chatie/python-wechaty",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
