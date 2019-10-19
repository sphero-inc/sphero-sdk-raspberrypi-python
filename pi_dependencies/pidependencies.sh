sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
python -m venv env
source env/bin/activate
pip install aiohttp
pip install requests
pip install websocket-client
pip install pytest-asyncio
pip install pytest
pip install twine
pip install pyserial
pip install pyserial-asyncio
