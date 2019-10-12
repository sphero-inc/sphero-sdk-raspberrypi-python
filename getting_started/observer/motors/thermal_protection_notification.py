import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum


rvr = SpheroRvrObserver()


def thermal_protection_handler(response):
    print('Motor thermal protection response:', response)

def main():
    """ This program demonstrates how to register a handler for a motor thermal protection notification, in the event
        RVR's motors are at risk of overheating.  In order to receive the notification, RVR's motors must be heavy use
        for an extended period.
    """

    try:
        rvr.wake()

        rvr.enable_motor_thermal_protection_status_notify(is_enabled=True)

        rvr.on_motor_thermal_protection_status_notify(handler=thermal_protection_handler)

        # Give RVR time to wake up
        time.sleep(2)

        print('Press CTRL+C to stop this program anytime.')

        while True:
            rvr.raw_motors(
                left_mode=RawMotorModesEnum.forward.value,
                left_speed=128,  # Valid speed values are 0-255
                right_mode=RawMotorModesEnum.forward.value,
                right_speed=128  # Valid speed values are 0-255
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
