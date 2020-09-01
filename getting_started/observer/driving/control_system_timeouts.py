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
    """ This program demonstrates the use of control system timeouts.
    """
    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Register the handler for the stopped notification
        rvr.on_robot_has_stopped_notify(handler=stopped_handler)

        # Reset yaw
        rvr.reset_yaw()

        # Make sure that we're starting with the default timeout (2 seconds). This is
        # redundant, unless the timeouts have already been adjusted since boot.
        rvr.restore_default_control_system_timeout()


        print("Driving forward with the default 2 second timeout")

        rvr.drive_rc_si_units(
            linear_velocity=.3,     # Valid velocity values are in the range of [-2..2] m/s
            yaw_angular_velocity=0, # RVR will spin at up to 624 degrees/s.  Values outside of [-624..624] will saturate internally.
            flags=0
        )

        # Delay to allow RVR to drive
        time.sleep(4)

        # The control system timeout can be modified to keep a command running longer
        # or shorter than the default 2 seconds.  This remains in effect until changed back,
        # or until a reboot occurs. Note that this is in milliseconds.
        rvr.set_custom_control_system_timeout(command_timeout=4000)

        print("Turning left with timeout=4000 ms")
        # Continue driving forward, while turning left
        rvr.drive_rc_si_units(
            linear_velocity=.2,
            yaw_angular_velocity=20,
            flags=0
        )

        time.sleep(6)

        rvr.set_custom_control_system_timeout(command_timeout=1000)

        print("Turning right, with timeout=700 ms")

        # Continue driving forward, while turning right
        rvr.drive_rc_si_units(
            linear_velocity=.2,
            yaw_angular_velocity=-20,
            flags=0
        )

        # Delay to allow RVR to drive and come to a stop after the command times out
        time.sleep(2)

        # Restore the default timeout (2 seconds)
        rvr.restore_default_control_system_timeout()

        print("Driving forward again with default timeout restored")

        rvr.drive_rc_si_units(
            linear_velocity=.3,
            yaw_angular_velocity=0,
            flags=0
        )

        # Delay to allow RVR to drive and stop on its own when the command times out
        time.sleep(4)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
