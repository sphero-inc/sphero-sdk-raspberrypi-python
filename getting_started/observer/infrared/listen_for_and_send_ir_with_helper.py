import os
import sys
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import InfraredCodes


rvr = SpheroRvrObserver()


def infrared_message_received_handler(infrared_message):
    print('Infrared message response: ', infrared_message)


def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    """

    rvr.wake()

    # give RVR time to wake up
    time.sleep(2)

    rvr.infrared_control.listen_for_infrared_message(handler=infrared_message_received_handler)

    codes = [
        InfraredCodes.zero,
        InfraredCodes.one,
        InfraredCodes.two,
        InfraredCodes.three
    ]

    for _ in range(20):
        rvr.infrared_control.send_infrared_messages(
            messages=codes,
            strength=64
        )

        print('Infrared message sent with codes: {0}'.format([code.value for code in codes]))

        time.sleep(2)

    rvr.close()


if __name__ == '__main__':
    main()
