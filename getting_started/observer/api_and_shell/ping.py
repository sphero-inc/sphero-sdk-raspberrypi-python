import os
import sys
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import SpheroRvrTargets


rvr = SpheroRvrObserver()


def echo_handler(echo_response):
    print('Echo response: ', echo_response)


def main():
    """ This program demonstrates how to use the echo command, which sends data to RVR and RVR returns
        the same data. Echo can be used to check to see if RVR is connected and awake.
    """

    rvr.wake()

    # give RVR time to wake up
    time.sleep(2)

    rvr.echo(
        data=[2, 4, 16, 32, 64, 128, 255],
        handler=echo_handler,
        target=SpheroRvrTargets.primary.value
    )

    # sleep for one second such that RVR has time to send data back
    time.sleep(1)

    rvr.close()


if __name__ == '__main__':
    main()
