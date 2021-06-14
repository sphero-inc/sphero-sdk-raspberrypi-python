import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

# Flag used to indicate that calibration is complete
calibration_completed = False

# Initial yaw offset to magnetic North
yaw_north = 0

# Handler for completion of calibration
def on_calibration_complete_notify_handler(response):
    global calibration_completed

    print('Calibration complete, response:', response)
    calibration_completed = True


def main():
    """ This program demonstrates the following:
        1. Run magnetometer calibration to find the yaw angle of magnetic north
        2. Turn to face magnetic north
        3. Reset the yaw angle to zero at north
        4. Turn to face a compass heading
    """

    try:
        global calibration_completed
        global yaw_north

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

        print('Turning to face north')

        # Turn to face north
        rvr.drive_with_yaw_normalized(
            yaw_angle=yaw_north, # This is the target yaw angle, which RVR will turn to face.
            linear_velocity=0,   # This is normalized 0-255.  0 will cause RVR to turn in place
        )

        # Leave some time for it to complete the move
        time.sleep(2)

        # Reset yaw to zero.  After this, zero heading will be magnetic north
        rvr.reset_yaw()

        print('Turning to face east')

         # You can now drive along compass headings as follows (adjust linear velocity to drive forward)
        rvr.drive_with_heading(
            speed = 0,  # This is normalized 0-255.  0 will cause RVR to turn in place
            heading=90, # This is the compass heading
            flags=0     # Just leave this at zero to drive forward
        )

        # Allow some time for the move to complete before we end our script
        time.sleep(2)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
