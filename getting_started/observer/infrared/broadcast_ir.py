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

    rvr.wake()

    # give RVR time to wake up
    time.sleep(2)

    rvr.start_robot_to_robot_infrared_broadcasting(
        far_code=InfraredCodes.one.value,
        near_code=InfraredCodes.zero.value
    )

    for i in range(2):
        rvr.raw_motors(
            left_mode=RawMotorModesEnum.forward.value,
            left_speed=64,
            right_mode=RawMotorModesEnum.forward.value,
            right_speed=64
        )

        # delay to allow RVR to drive
        time.sleep(1)

    rvr.stop_robot_to_robot_infrared_broadcasting()

    rvr.close()


if __name__ == '__main__':
    main()
