import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import InfraredCodes
from sphero_sdk import RawMotorModesEnum


rvr = SpheroRvrObserver()


def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.start_robot_to_robot_infrared_broadcasting(
            far_code=InfraredCodes.one.value,
            near_code=InfraredCodes.zero.value
        )

        for i in range(2):
            rvr.raw_motors(
                left_mode=RawMotorModesEnum.forward.value,
                left_speed=64,  # Valid speed values are 0-255
                right_mode=RawMotorModesEnum.forward.value,
                right_speed=64  # Valid speed values are 0-255
            )

            # Delay to allow RVR to drive
            time.sleep(2)

    except:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.stop_robot_to_robot_infrared_broadcasting()

        # Delay to allow RVR issue command before closing
        time.sleep(.5)

        rvr.close()


if __name__ == '__main__':
    main()
