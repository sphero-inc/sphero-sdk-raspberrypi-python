import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def main():
    """
    This program has RVR drive using the function drive_with_heading with the reverse_drive flag set.
    It demonstrates how the heading (passed in as the second argument to the function) affects
    the driving direction when in reverse mode.

    Note:
        To have RVR drive, we call time.sleep(...); if we did not have these calls, the program would
        go on and execute all statements and exit without the driving ever taking place.
    """
    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # Reset yaw such that the heading will be set compared to the direction RVR is currently facing
    rvr.reset_yaw()

    # If driving in reverse mode, the heading is relative to the direction that the BACK of RVR is facing
    rvr.drive_with_heading(128, 90, 1)
    time.sleep(1)

    # Stop RVR
    rvr.raw_motors(0, 0, 0, 0)

    rvr.close()

main()