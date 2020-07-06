import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

# Flag used to indicate that calibration is complete
calibration_completed = False


# Handler for completion of calibration
def on_calibration_complete_notify_handler(response):
    global calibration_completed

    print('Calibration complete, response:', response)
    calibration_completed = True


def main():
    """ This program demonstrates the magnetometer calibration to find north.
    """

    try:
        global calibration_completed

        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Register for the async on completion of calibration
        rvr.on_magnetometer_calibration_complete_notify(handler=on_calibration_complete_notify_handler)

        # Begin calibration
        print('Begin magnetometer calibration to find North...')
        rvr.magnetometer_calibrate_to_north()

        # Wait to complete the calibration.  Note: In a real project, a timeout mechanism
        # should be here to prevent the script from getting caught in an infinite loop
        while not calibration_completed:
            time.sleep(0)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
