import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum


rvr = SpheroRvrObserver()


def main():
    """ This program has RVR drive around in different directions.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()

        rvr.raw_motors(
            left_mode=RawMotorModesEnum.forward.value,
            left_speed=128,  # Valid speed values are 0-255
            right_mode=RawMotorModesEnum.forward.value,
            right_speed=128  # Valid speed values are 0-255
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        rvr.raw_motors(
            left_mode=RawMotorModesEnum.reverse.value,
            left_speed=64,  # Valid speed values are 0-255
            right_mode=RawMotorModesEnum.reverse.value,
            right_speed=64  # Valid speed values are 0-255
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        rvr.raw_motors(
            left_mode=RawMotorModesEnum.reverse.value,
            left_speed=128,  # Valid speed values are 0-255
            right_mode=RawMotorModesEnum.forward.value,
            right_speed=128  # Valid speed values are 0-255
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        rvr.raw_motors(
            left_mode=RawMotorModesEnum.forward.value,
            left_speed=128,  # Valid speed values are 0-255
            right_mode=RawMotorModesEnum.forward.value,
            right_speed=128  # Valid speed values are 0-255
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        rvr.raw_motors(
            left_mode=RawMotorModesEnum.off.value,
            left_speed=0,  # Valid speed values are 0-255
            right_mode=RawMotorModesEnum.off.value,
            right_speed=0  # Valid speed values are 0-255
        )

        # Delay to allow RVR to drive
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
