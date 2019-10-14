import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum


rvr = SpheroRvrObserver()


def motor_fault_handler(response):
    print('Motor fault response:', response)

def main():
    """ In the rare event that a motor fault occurs while operating RVR, this program demonstrates how to register
        a handler for a motor fault notification.  In order to receive a motor fault notification, RVR's motors
        must be in use.
    """

    try:
        rvr.wake()

        rvr.enable_motor_fault_notify(is_enabled=True)

        rvr.on_motor_fault_notify(handler=motor_fault_handler)

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

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
