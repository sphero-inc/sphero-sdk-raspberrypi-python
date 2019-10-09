import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def will_sleep_handler():
    print('RVR is about to sleep...')

    # here we could issue a command to RVR, e.g. wake() such that the sleep timer is reset


def did_sleep_handler():
    print('RVR is asleep...')


def main():
    """ This program demonstrates how to register handlers for a) the event received 10 seconds
        before RVR will sleep unless some new command is issued and b) the event received
        when RVR does go to sleep.

        Note that these notifications are received without the need to enable them on the robot.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.on_will_sleep_notify(will_sleep_handler)

        rvr.on_did_sleep_notify(did_sleep_handler)

        # Sleep for 310 seconds such that we see the aforementioned events have time to occur
        time.sleep(310)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
