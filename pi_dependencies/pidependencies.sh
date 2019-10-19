sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
python -m venv env
source env/bin/activate
pip3 install aiohttp
pip3 install requests
pip3 install websocket-client
pip3 install pytest-asyncio
pip3 install pytest
pip3 install twine
pip3 install pyserial
pip3 install pyserial-asyncio
