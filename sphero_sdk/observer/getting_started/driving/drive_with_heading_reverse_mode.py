import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def main():
    """
    Note:
        To have RVR drive, we call time.sleep(...); if we did not have these calls, the program would
        go on and execute all statements and exit without the driving ever taking place.
    """
    rvr.wake()

    # Reset yaw such that the heading will be set compared to the direction RVR is currently facing
    rvr.reset_yaw()

    # If driving in reverse mode, the heading is relative to the direction that the BACK of RVR is facing
    rvr.drive_with_heading(128, 90, 1)
    time.sleep(1)

    # Stop RVR
    rvr.raw_motors(0, 0, 0, 0)

main()