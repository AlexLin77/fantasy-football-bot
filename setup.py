# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='ffbot',
    version='2.0.0',
    description='Fantasy football draft simulator and assistant',
    long_description=(here / 'README.md').read_text(encoding='utf-8'),
    author='Alex Lin',
    author_email='alexjlin77@gmail.com',
    url='https://github.com/AlexLin77/fantasy-football-bot',
    license=license,
    packages=find_packages(exclude=('tests')),
    install_requires=['pandas==1.1.0', 'requests==2.23.0']
)

