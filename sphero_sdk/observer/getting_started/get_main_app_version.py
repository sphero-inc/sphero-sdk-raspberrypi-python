import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def handler(major, minor, revision):
    print('{} {}.{}.{}'.format("Nordic", major, minor, revision))

rvr.get_main_application_version(handler, target=1)
rvr.get_main_application_version(handler, target=2)

