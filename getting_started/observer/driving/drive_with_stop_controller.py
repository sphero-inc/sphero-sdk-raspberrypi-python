import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import XyPositionDriveFlagsBitmask

rvr = SpheroRvrObserver()

# Flags for simple event waiting
target_position_reached = False
rvr_has_stopped = False

# This is the reponse handler
def get_stop_controller_state_response_handler(response):
    global rvr_has_stopped
    rvr_has_stopped = response["stopped"]


# Handler for the active controller stopped notification.
# Regardless of how your instruct your robot to stop,
# your program can wait for this to confirm that the robot
# has come to a stop.
def stopped_handler():
    global rvr_has_stopped
    print("RVR has stopped")
    rvr_has_stopped = True


def on_xy_position_drive_result_notify_handler(response):
    global target_position_reached

    # To keep things simpler, just assume success.  No error handling
    # for this example.
    target_position_reached = True


def return_to_start():
    global target_position_reached

    print("Returning to (0,0,0)")

    # Note: the normalized and SI drive to position commands specify end conditions
    # explicitly, so they are exceptions to the rule and bypass the control system timeout.
    rvr.drive_to_position_si(
        yaw_angle=0,
        x=0,
        y=0,
        linear_speed=.5,
        flags=XyPositionDriveFlagsBitmask.auto_reverse
    )

    while not target_position_reached:
        time.sleep(0)

    # Clear the flag
    target_position_reached = False


def main():
    """ This program demonstrates the use of the stop controller.
    """
    try:
        global rvr_has_stopped

        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Register the handler for the xy position drive result notification
        rvr.on_xy_position_drive_result_notify(
            handler=on_xy_position_drive_result_notify_handler
        )

        # Reset yaw
        rvr.reset_yaw()

        # Reset the locator too
        rvr.reset_locator_x_and_y()

        # Start by setting the control system timeout to 10 seconds, just to get it
        # out of the way.
        rvr.set_custom_control_system_timeout(command_timeout=10000)

        print("Driving forward...")
        rvr.drive_rc_si_units(
            linear_velocity=1,      # Valid velocity values are in the range of [-1.555..1.555] m/s
            yaw_angular_velocity=0, # RVR will spin at up to 624 degrees/s.  Values outside of [-624..624] will saturate internally.
            flags=0
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        print("Requesting a stop with default deceleration")

        # This will request a stop with default deceleration.
        # Control of the motors is handed off to the stop controller,
        # which linearly ramps down the velocity targets of both treads.
        rvr.drive_stop()

        # It's possible to poll whether the robot has come to a stop.
        # We'll poll the stop controller state to decide when to continue.
        rvr_has_stopped = False
        while not rvr_has_stopped:
            rvr.get_stop_controller_state(handler=get_stop_controller_state_response_handler)
            time.sleep(0.2)  # Some delay here is required to avoid flooding the UART

        # Now clear the flag
        rvr_has_stopped = False

        # Pause for a second for visibility
        time.sleep(1)

        # Return to our starting position and orientation.
        return_to_start()

        print("Driving forward...")
        rvr.drive_rc_si_units(
            linear_velocity=1,
            yaw_angular_velocity=0,
            flags=0
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        print("Requesting a stop with gentle deceleration")
        # This will request a stop with slower than normal deceleration.
        # Control of the motors is handed off to the stop controller,
        # which linearly ramps down the velocity targets of both treads.
        rvr.drive_stop_custom_decel(
            deceleration_rate=0.5 # Decelerate both treads toward 0 velocity at 0.5 m/s^2
        )

        # In addition to polling to check if the robot has stopped,
        # We can also register a handler for a notification.
        rvr.on_robot_has_stopped_notify(handler=stopped_handler)

        # Wait until we receive the notification that the robot has stopped.
        while not rvr_has_stopped:
            time.sleep(0)

        # Now clear the flag
        rvr_has_stopped = False

        # Pause for a second for visibility
        time.sleep(1)

        # Return to our starting position and orientation.
        return_to_start()

        print("Driving forward...")
        rvr.drive_rc_si_units(
            linear_velocity=1,
            yaw_angular_velocity=0,
            flags=0
        )

        # Delay to allow RVR to drive
        time.sleep(1)

        print("Requesting a stop with rapid deceleration")
        # This will request a stop with faster than normal deceleration.
        # Control of the motors is handed off to the stop controller,
        # which linearly ramps down the velocity targets of both treads.
        rvr.drive_stop_custom_decel(
            deceleration_rate=10 # Decelerate both treads toward 0 velocity at 10 m/s^2
        )

        # Wait until we receive the notification that the robot has stopped.
        while not rvr_has_stopped:
            time.sleep(0)

        # Politely restore the default timeout (2 seconds)
        rvr.restore_default_control_system_timeout()

        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
