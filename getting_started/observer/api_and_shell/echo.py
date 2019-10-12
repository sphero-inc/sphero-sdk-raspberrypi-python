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
        the same data. Echo can be used to check to see if RVR is connected.  RVR does not need to be awake
        for this operation.
    """

    rvr.echo(
        data=[0, 1, 2],
        handler=echo_handler,
        target=SpheroRvrTargets.primary.value
    )

    # Give RVR time to respond
    time.sleep(1)

    rvr.echo(
        data=[3, 4, 5],
        handler=echo_handler,
        target=SpheroRvrTargets.secondary.value
    )

    # Sleep for one second such that RVR has time to send data back
    time.sleep(1)

    rvr.close()


if __name__ == '__main__':
    main()
