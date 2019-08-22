import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import DriveControlObserver
rvr = SpheroRvrObserver()

driver = DriveControlObserver(rvr)

def main():
    """ This program has RVR drive around in different directions using raw motors.

    Note:
        To give RVR time to drive, we call time.sleep(...); if we did not have these calls, the program would
        go on and execute all the statements and exit without the driving ever taking place.
    """

    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    # Set aiming lights
    driver.aim_start()

    # Reset yaw such that the heading will be set compared to the direction RVR is currently facing
    driver.reset_heading()

    # Drive forward at speed 64 for one second
    driver.drive_forward_seconds(64, 0, 1)

    # Drive backwards at speed 64 for one second
    driver.drive_backward_seconds(64, 0, 1)

    # Turn left
    driver.turn_left_degrees(0, 90)

    # Turn off aiming lights
    driver.aim_stop()

    # Stop RVR
    # rvr.raw_motors(0, 0, 0, 0)

    rvr.close()


main()
