import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import SpheroRvrTargets


rvr = SpheroRvrObserver()


def get_nordic_main_application_version_handler(nordic_main_application_version):
    print('Nordic main application version (target 1): ', nordic_main_application_version)


def get_st_main_application_version_handler(st_main_application_version):
    print('ST main application version (target 2): ', st_main_application_version)


def main():
    """ This program demonstrates how to obtain the firmware version for a specific processor.  RVR does not need
        to be awake for this operation.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.get_main_application_version(
            handler=get_nordic_main_application_version_handler,
            target=SpheroRvrTargets.primary.value
        )

        # Sleep for one second such that RVR has time to send data back
        time.sleep(1)

        rvr.get_main_application_version(
            handler=get_st_main_application_version_handler,
            target=SpheroRvrTargets.secondary.value
        )

        # Sleep for one second such that RVR has time to send data back
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
