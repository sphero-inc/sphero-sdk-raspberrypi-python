import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum


rvr = SpheroRvrObserver()


def motor_fault_handler(response):
    print('Motor fault state response:', response)

def main():
    """ In the rare event that a motor fault occurs, this program demonstrates how to retrieve the motor fault state
        on RVR. In order to detect a motor fault, there must be an attempt to use them.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.raw_motors(
            left_mode=RawMotorModesEnum.forward.value,
            left_speed=128,  # Valid speed values are 0-255
            right_mode=RawMotorModesEnum.forward.value,
            right_speed=128  # Valid speed values are 0-255
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        rvr.get_motor_fault_state(handler=motor_fault_handler)

        # Delay to allow callback
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
