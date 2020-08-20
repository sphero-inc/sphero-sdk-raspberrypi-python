import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

# Handler for the active controller stopped notification.
# After sending a stop command, your program can wait for
# this async to confirm that the robot has come to a stop
def stopped_handler():
    print('RVR has stopped')


def main():
    """ This program has RVR drive around using the normalized RC drive command.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Register the handler for the stopped notification
        rvr.on_robot_has_stopped_notify(handler=stopped_handler)

        rvr.reset_yaw()

        print("sending drive command")

        rvr.drive_rc_normalized(
            linear_velocity=20,  # Valid linear velocity values are -127..127
            yaw_angular_velocity=0,  # Valid angular velocity values are -127..127
            flags=0
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        # Continue driving forward, while turning left
        rvr.drive_rc_normalized(
            linear_velocity=20,         # Valid linear velocity values are -127..127
            yaw_angular_velocity=20,    # Valid angular velocity values are -127..127
            flags=0
        )

        # Delay to allow RVR to turn
        time.sleep(1)

        # Drive in new forward direction
        rvr.drive_rc_normalized(
            linear_velocity=20,  # Valid linear velocity values are -127..127
            yaw_angular_velocity=0,  # Valid angular velocity values are -127..127
            flags=0
        )

        # Delay to allow RVR to drive
        time.sleep(2)

        print("sending stop command")

        # Stop driving, with deceleration rate of 2 m/s^2
        rvr.drive_stop(2.0)

        # Delay to allow RVR to stop
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
