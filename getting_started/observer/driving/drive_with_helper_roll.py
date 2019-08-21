import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import DriveControlObserver

rvr = SpheroRvrObserver()

driver = DriveControlObserver(rvr)


def main():
    """ This program has RVR drive with roll, using the helper functions defined in DriveControlObserver.

    Note:
        To give RVR time to drive, we call time.sleep(...); if we did not have these calls, the program would
        go on and execute all the statements and exit without the driving ever taking place.
    """

    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # Reset yaw such that the heading will be set compared to the direction RVR is currently facing
    driver.reset_heading()

    # Turn right degrees and drive for 1.5 seconds
    driver.roll_start(64, 90)
    time.sleep(1.5)

    # Turn left (relative to original heading) and stop
    driver.roll_stop(270)
    time.sleep(2)

    rvr.close()


main()
