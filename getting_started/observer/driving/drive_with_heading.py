import os
import sys
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import DriveFlagsBitmask


rvr = SpheroRvrObserver()


def main():
    """ This program has RVR drive around in different directions using the function drive_with_heading.
    """

    rvr.wake()

    # give RVR time to wake up
    time.sleep(2)

    rvr.reset_yaw()

    rvr.drive_with_heading(
        speed=128,
        heading=0,
        flags=DriveFlagsBitmask.none.value
    )

    # delay to allow RVR to drive
    time.sleep(1)

    rvr.drive_with_heading(
        speed=128,
        heading=0,
        flags=DriveFlagsBitmask.drive_reverse.value
    )

    # delay to allow RVR to drive
    time.sleep(1)

    rvr.drive_with_heading(
        speed=128,
        heading=90,
        flags=DriveFlagsBitmask.none.value
    )

    # delay to allow RVR to drive
    time.sleep(1)

    rvr.drive_with_heading(
        speed=128,
        heading=270,
        flags=DriveFlagsBitmask.none.value
    )

    # delay to allow RVR to drive
    time.sleep(1)

    rvr.drive_with_heading(
        speed=0,
        heading=0,
        flags=DriveFlagsBitmask.none.value
    )

    # delay to allow RVR to drive
    time.sleep(1)

    rvr.close()


if __name__ == '__main__':
    main()
