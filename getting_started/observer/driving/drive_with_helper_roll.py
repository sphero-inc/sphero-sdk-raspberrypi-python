import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def main():
    """ This program has RVR drive with how to drive RVR using the drive control helper.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.drive_control.reset_heading()

        rvr.drive_control.roll_start(
            speed=64,
            heading=90
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        rvr.drive_control.roll_stop(heading=270)

        # Delay to allow RVR to drive
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
