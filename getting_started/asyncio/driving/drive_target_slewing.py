import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import LinearVelocitySlewMethodsEnum


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

# Flag for tracking position move completion
move_completed = False

# Handler for completion of XY position drive moves.
# In this script it is only used for returning to our starting position
async def on_xy_position_drive_result_notify_handler(response):
    global move_completed

    move_completed = True
    print('Move completed, response:', response)


# This wrapper function implements a simple way to return to the start position
async def return_to_start():
    global move_completed

    await rvr.drive_stop()

    # Allow RVR some time to come to a stop
    await asyncio.sleep(1.5)

    print("Driving to (0,0) at 0 degrees")

    # Clear the completion flag
    move_completed = False

    # Send the drive command, passing the wrapper function parameters into the matching
    # parameters in rvr.drive_to_position_normalized (which sends the actual drive command)
    await rvr.drive_to_position_normalized(
        yaw_angle=0,             # 0 degrees is straight ahead, +CCW (Following the right hand rule)
        x=0,                             # Target position X coordinate in meters
        y=0,                             # Target position Y coordinate in meters
        linear_speed=64,       # Max speed in transit to target.  Normalized in the range [0..127]
        flags=0,                         # Option flags (none applied here)
    )

    # Wait to complete the move.  Note: In a real project, a timeout mechanism
    # should be here to prevent the script from getting caught in an infinite loop
    while not move_completed:
        await asyncio.sleep(0)


# This function gives us an easily repeated driving sequence to compare different target slewing configurations
async def drive_demo():
    await rvr.drive_with_yaw_si(
        linear_velocity=.5,
        yaw_angle=0  # Valid yaw values are traditionally [-179..+180], but will continue wrapping outside of that range
    )

    await asyncio.sleep(1)

    await rvr.drive_with_yaw_si(
        linear_velocity=1,
        yaw_angle=-90  # Valid yaw values are traditionally [-179..+180], but will continue wrapping outside of that range
    )

    await asyncio.sleep(2)

    # Drive back to the starting position using the XY position controller, which also uses yaw target slewing
    await return_to_start()


async def main():
    """ This program demonstrates RVR's adjustable drive target slewing feature.

        Yaw and linear velocity slewing behaviors can be adjusted independently.

        Note:  Make sure you have plenty of space ahead and to the right of RVR from the starting position.

        See control system documentation at sdk.sphero.com for more details 
        on the meaning of each parameter.  This example will demonstrate some example
        configurations from the docs.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.reset_yaw()

    await rvr.reset_locator_x_and_y();

    # Register for the async on completion of xy position drive commands
    await rvr.on_xy_position_drive_result_notify(handler=on_xy_position_drive_result_notify_handler)

    await rvr.restore_default_control_system_timeout()

    # Make sure that we're starting with the default slew parameters.
    # This can be used at any time to restore the default slewing behavior
    await rvr.restore_default_drive_target_slew_parameters()

    # Get the default parameters and print them
    response = await rvr.get_drive_target_slew_parameters()
    print(response)

    # Drive with the default slew parameters.
    await drive_demo()

    # Set RVR to always turn slowly regardless of linear velocity
    await rvr.set_drive_target_slew_parameters(
        a=0,
        b=0,
        c=60,
        linear_acceleration=.500,       # This will set a linear acceleration of .5 m/s^2
        linear_velocity_slew_method=LinearVelocitySlewMethodsEnum.constant
    )

    # Set an extra long timeout to accomodate additional turning time
    await rvr.set_custom_control_system_timeout(3000)

    # Drive with the updated parameters
    await drive_demo()

    # Set RVR to turn faster as linear speed increases.
    # Also give it some snappier linear acceleration.
    await rvr.set_drive_target_slew_parameters(
        a=-30,
        b=400,
        c=100,
        linear_acceleration=3,       # This will set a linear acceleration of 3 m/s^2
        linear_velocity_slew_method=LinearVelocitySlewMethodsEnum.constant
    )

    # Drive with the updated parameters
    await drive_demo()

    await rvr.close()


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
