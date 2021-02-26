from io import open
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version_dict = {}
with open(path.join(here, 'sphero_sdk', '__version__.py')) as f:
    exec(f.read(), version_dict)
    print('Version: {}'.format(version_dict))


setup(
    author='Sphero',
    name='sphero_sdk',
    version=version_dict['__version__'],
    author_email='sdk@sphero.com',
    url='sdk.sphero.com',
    description='Provides an API for interfacing with Sphero RVR',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.5.3',
    packages=find_packages(),
    classifiers=[
         'Programming Language :: Python :: 3',
         'License :: Other/Proprietary License',
         'Operating System :: OS Independent',
     ],
    install_requires=[
        'aiohttp == 3.7.4',
        'requests == 2.21.0',
        'websocket-client == 0.54.0',
        'pyserial == 3.4',
        'pyserial-asyncio == 0.4',
        'twine == 1.13.0'
    ]
)
