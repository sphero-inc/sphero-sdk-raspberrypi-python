import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def get_magnetometer_reading_response_handler(response):
    print('Magnetometer reading response: ', response)


def main():
    """ This program demonstrates how to get a reading from the magnetometer on RVR.
    """
    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.get_magnetometer_reading(handler=get_magnetometer_reading_response_handler)

        # Keep the script running briefly so we actually get to report the response.
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
