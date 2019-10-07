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

        # give RVR time to wake up
        time.sleep(2)

        rvr.drive_control.reset_heading()

        rvr.drive_control.drive_forward_seconds(
            speed=64,
            heading=0,
            time_to_drive=1
        )

        # delay to allow RVR to drive
        time.sleep(1)

        rvr.drive_control.drive_backward_seconds(
            speed=64,
            heading=0,
            time_to_drive=1
        )

        # delay to allow RVR to drive
        time.sleep(1)

        rvr.drive_control.turn_left_degrees(
            heading=0,
            amount=90
        )

        # delay to allow RVR to drive
        time.sleep(1)

    except KeyboardInterrupt:
        print('Program terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
