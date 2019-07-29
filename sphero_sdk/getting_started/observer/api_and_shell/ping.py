import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def handler(**kwargs):
    print(kwargs)

def main():
    """ This program demonstrates how to use the echo command, which sends data to RVR and has RVR return
    the same data. Echo can be used to check to see if RVR is connected and awake.

    """
    rvr.wake()

    rvr.echo(255, handler, 1)

    # Sleep for one second such that RVR has time to send data back
    time.sleep(1)

    rvr.close()

main()