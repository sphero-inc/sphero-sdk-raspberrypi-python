import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr
from sphero_sdk import SerialAsyncDal

rvr = ObserverSpheroRvr()

def main():
    """
    Note:
        To give RVR time to drive, we call asyncio.sleep(...); if we did not have these calls, the program would 
        go on and execute all the statements and exit without the driving ever taking place. 
    """
    rvr.wake()

    # Drive straight for one second at speed 128
    rvr.raw_motors(1, 128, 1, 128)
    time.sleep(1)

    # Drive backwards for one second at speed 64
    rvr.raw_motors(2, 128, 2, 128)
    time.sleep(1)

    # Turn right
    rvr.raw_motors(2, 128, 1, 128)
    time.sleep(0.75)

    # Drive forward for 1 second at speed 128
    rvr.raw_motors(1, 128, 1, 128)
    time.sleep(1)

    # Stop RVR
    rvr.raw_motors(0, 0, 0, 0)

try:
    main()
except KeyboardInterrupt:
    sys.exit()