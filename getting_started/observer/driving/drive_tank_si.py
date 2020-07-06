import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def main():
    """ This program has RVR drive around in different directions using the function drive_tank_si.
        This function commands a floating point linear velocity target for each tread in meters per second.
        Achievable velocity targets are in the range of [-1.555..1.555]
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()

        # drive forward, 50% speed
        rvr.drive_tank_si_units(
            left_velocity=0.75,  # Valid velocity values are [-1.555..1.555]
            right_velocity=0.75
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        # drive reverse, ~50% speed
        rvr.drive_tank_si_units(
            left_velocity=-0.75,
            right_velocity=-0.75
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        # Spin in place slowly
        rvr.drive_tank_si_units(
            left_velocity=0.1,
            right_velocity=-0.1
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        # Spin in place quickly
        rvr.drive_tank_si_units(
            left_velocity=-1.5,
            right_velocity=1.5
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        rvr.drive_tank_si_units(
            left_velocity=0,
            right_velocity=0
        )

        # Delay to allow RVR to drive
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
