import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def main():
    """ This program has RVR drive around in different directions using drive_with_heading.

    Note:
        To have RVR drive, we call time.sleep(...); if we did not have these calls, the program would
        go on and execute all statements and exit without the driving ever taking place.
    """
    rvr.wake()

    # Reset yaw such that the heading will be set compared to the direction RVR is currently facing
    rvr.reset_yaw()

    # Drive straight for one second at speed 128
    rvr.drive_with_heading(128, 0, 0)
    time.sleep(1)

    # Drive backwards for one second at speed 128
    # Note that the flag is set to 1 for reverse
    rvr.drive_with_heading(128, 0, 1)
    time.sleep(1)

    # Go right for a second (relative to original yaw)
    rvr.drive_with_heading(128, 90, 0)
    time.sleep(1)

    # Go left for a second (relative to original yaw)
    rvr.drive_with_heading(128, 270, 0)
    time.sleep(1)

    # Go back to original position
    rvr.drive_with_heading(0, 0, 0)
    time.sleep(1)

    # Stop RVR
    rvr.raw_motors(0,0,0,0)

    rvr.close()

main()
