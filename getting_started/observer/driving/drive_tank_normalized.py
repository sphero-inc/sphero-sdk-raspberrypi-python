import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def main():
    """ This program has RVR drive around in different directions using the function drive_tank_normalized.
        This function commands a normalized linear velocity target for each tread.  Velocity targets
        are normalized in the range [-127..127]
    """
    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()

        # drive forward, 50% speed
        rvr.drive_tank_normalized(
            left_velocity=64,  # Valid velocity values are [-127..127]
            right_velocity=64  # Valid velocity values are [-127..127]
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        # drive reverse, 50% speed
        rvr.drive_tank_normalized(
            left_velocity=-64,  # Valid velocity values are [-127..127]
            right_velocity=-64  # Valid velocity values are [-127..127]
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        # Spin in place slowly
        rvr.drive_tank_normalized(
            left_velocity=5,  # Valid velocity values are [-127..127]
            right_velocity=-5 # Valid velocity values are [-127..127]
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        # Spin in place quickly
        rvr.drive_tank_normalized(
            left_velocity=-127,  # Valid velocity values are [-127..127]
            right_velocity=127  # Valid velocity values are [-127..127]
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        rvr.drive_tank_normalized(
            left_velocity=0,  # Valid velocity values are [-127..127]
            right_velocity=0  # Valid velocity values are [-127..127]
        )

        # Delay to allow RVR to drive
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()