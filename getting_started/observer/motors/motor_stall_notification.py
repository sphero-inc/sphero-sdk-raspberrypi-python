import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum


rvr = SpheroRvrObserver()


def motor_stall_handler(response):
    print('Motor stall response:', response)

def main():
    """ This program demonstrates how to receive motor stall notifications, in the event that RVR's treads become
        obstructed, and is unable to move.  In order to receive the notification, RVR's motors must be in use.
    """

    try:
        rvr.wake()

        rvr.enable_motor_stall_notify(is_enabled=True)

        rvr.on_motor_stall_notify(handler=motor_stall_handler)

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
