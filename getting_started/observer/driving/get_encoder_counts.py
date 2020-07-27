import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def get_encoder_counts_response_handler(response):
    print('Encoder counts response: ', response)


def main():
    """ This program demonstrates how to get encoder counts on RVR.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.get_encoder_counts(handler=get_encoder_counts_response_handler)

        # Give RVR time to respond
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
