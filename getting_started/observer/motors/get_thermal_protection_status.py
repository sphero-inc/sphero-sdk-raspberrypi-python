import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RawMotorModesEnum


rvr = SpheroRvrObserver()


def thermal_protection_handler(response):
    print('Thermal protection status response', response)

def main():
    """ This program demonstrates how to get motor thermal protection status, in the event RVR's motors have already
        been stopped to prevent overheating.  This can be used to check if the motors are no longer in a thermal
        protection state. RVR does not need to be awake in order to run this operation.
    """

    try:
        rvr.get_motor_fault_state(handler=thermal_protection_handler)

        # Delay to allow the callback to be invoked
        time.sleep(2)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
