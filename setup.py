#!/usr/bin/env python3
from setuptools import find_packages
from distutils.core import setup

setup(
	name='sphero_sdk',
	version='0.3.4.post2',  # TODO: unify with __version__.py
	description='Sphero SDK to run on Raspberry Pi using Python',
	author='Anthony Vizcarra',
	author_email='Anthony@sphero.com',
	url='https://github.com/sphero-inc/sphero-sdk-raspberrypi-python',
	packages=find_packages(include=['sphero_sdk*']),
	install_requires=[
		'aiohttp',
		'pyserial',
		'pyserial-asyncio',
	],
)