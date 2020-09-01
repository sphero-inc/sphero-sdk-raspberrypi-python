import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import LinearVelocitySlewMethodsEnum


rvr = SpheroRvrObserver()

# Flag for tracking position move completion
move_completed = False

# Handler for completion of XY position drive moves.
# In this script it is only used for returning to our starting position
def on_xy_position_drive_result_notify_handler(response):
    global move_completed

    move_completed = True
    print('Move completed, response:', response)

def get_drive_target_slew_parameters_handler(response):
    print('Drive target slew parameters:', response)

# This wrapper function implements a simple way to return to the start position
def return_to_start():
    global move_completed

    rvr.drive_stop()

    # Allow RVR some time to come to a stop
    time.sleep(1.5)

    print("Driving to (0,0) at 0 degrees")

    # Clear the completion flag
    move_completed = False

    # Send the drive command, passing the wrapper function parameters into the matching
    # parameters in rvr.drive_to_position_normalized (which sends the actual drive command)
    rvr.drive_to_position_normalized(
        yaw_angle=0,             # 0 degrees is straight ahead, +CCW (Following the right hand rule)
        x=0,                             # Target position X coordinate in meters
        y=0,                             # Target position Y coordinate in meters
        linear_speed=64,       # Max speed in transit to target.  Normalized in the range [0..127]
        flags=0,                         # Option flags (none applied here)
    )

    # Wait to complete the move.  Note: In a real project, a timeout mechanism
    # should be here to prevent the script from getting caught in an infinite loop
    while not move_completed:
        time.sleep(0)


# This function gives us an easily repeated driving sequence to compare different target slewing configurations
def drive_demo():
    rvr.drive_with_yaw_si(
        linear_velocity=.5,
        yaw_angle=0  # Valid yaw values are traditionally [-179..+180], but will continue wrapping outside of that range
    )

    time.sleep(1)

    rvr.drive_with_yaw_si(
        linear_velocity=1,
        yaw_angle=-90  # Valid yaw values are traditionally [-179..+180], but will continue wrapping outside of that range
    )

    time.sleep(2)

    # Drive back to the starting position using the XY position controller, which also uses yaw target slewing
    return_to_start()


def main():
    """ This program demonstrates RVR's adjustable drive target slewing feature.

        Yaw and linear velocity slewing behaviors can be adjusted independently.

        Note:  Make sure you have plenty of space ahead and to the right of RVR from the starting position.

        See control system documentation at sdk.sphero.com for more details 
        on the meaning of each parameter.  This example will demonstrate some example
        configurations from the docs.
    """
    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.reset_yaw()

        rvr.reset_locator_x_and_y();

        # Register for the async on completion of xy position drive commands
        rvr.on_xy_position_drive_result_notify(
            handler=on_xy_position_drive_result_notify_handler
        )

        rvr.restore_default_control_system_timeout()

        # Make sure that we're starting with the default slew parameters.
        # This can be used at any time to restore the default slewing behavior
        rvr.restore_default_drive_target_slew_parameters()

        print('Getting default drive target slew parameters...')
        # Get the default parameters and print them
        response = rvr.get_drive_target_slew_parameters(
            handler=get_drive_target_slew_parameters_handler
        )
        print(response)

        # Drive with the default slew parameters.
        drive_demo()

        # Set RVR to always turn slowly regardless of linear velocity
        rvr.set_drive_target_slew_parameters(
            a=0,
            b=0,
            c=60,
            linear_acceleration=.500,       # This will set a linear acceleration of .5 m/s^2
            linear_velocity_slew_method=LinearVelocitySlewMethodsEnum.constant
        )

        # Set an extra long timeout to accomodate additional turning time
        rvr.set_custom_control_system_timeout(3000)

        # Drive with the updated parameters
        drive_demo()

        # Set RVR to turn faster as linear speed increases.
        # Also give it some snappier linear acceleration.
        rvr.set_drive_target_slew_parameters(
            a=-30,
            b=400,
            c=100,
            linear_acceleration=3,       # This will set a linear acceleration of 3 m/s^2
            linear_velocity_slew_method=LinearVelocitySlewMethodsEnum.constant
        )

        # Drive with the updated parameters
        drive_demo()

        # Delay to make sure that any responses came back
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
