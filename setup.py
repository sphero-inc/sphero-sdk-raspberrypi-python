from io import open
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version_dict = {}
with open(path.join(here, 'spheroboros', '__version__.py')) as f:
    exec(f.read(), version_dict)
    print('Version: {}'.format(version_dict))


setup(
    name='spheroboros',
    author='Sphero',
    author_email='rvr_hackathon_external_user@sphero.com',
    url='www.sphero.com',
    version=version_dict['__version__'],
    description='Provides methods for interfacing with the Sphero Service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.5.3',
    packages=find_packages(),
    install_requires=[
        'aiohttp == 3.5.4',
        'requests == 2.21.0',
        'websocket-client == 0.54.0',
        'pyserial == 3.4',
        'pyserial-asyncio == 0.4'
    ]
)
