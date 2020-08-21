import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import XyPositionDriveFlagsBitmask


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

# Flags for simple event waiting
target_position_reached = False
rvr_has_stopped_from_handler = False

# Handler for the active controller stopped notification.
# After sending a stop command, your program can wait for
# this async to confirm that the robot has come to a stop
async def stopped_handler():
    global rvr_has_stopped_from_handler
    print("RVR has stopped")
    rvr_has_stopped_from_handler=True

async def on_xy_position_drive_result_notify_handler(response):
    global target_position_reached

    # To keep things simpler, just assume success.  No error handling
    # for this example.
    target_position_reached=True

async def return_to_start():
    global target_position_reached

    print("Returning to (0,0,0)")

    # Note: the normalized and SI drive to position commands specify end conditions
    # explicitly, so they are exceptions to the rule and bypass the control system timeout.
    await rvr.drive_to_position_si(
        yaw_angle=0,
        x=0,
        y=0,
        linear_speed=.5,
        flags=XyPositionDriveFlagsBitmask.auto_reverse
    )

    while not target_position_reached:
        await asyncio.sleep(0)

    # Clear the flag
    target_position_reached = False


async def main():
    """ This program demonstrates the use of the stop controller.
    """

    global rvr_has_stopped_from_handler

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Register the handler for the stopped notification
    await rvr.on_robot_has_stopped_notify(handler=stopped_handler)

    # Register the handler for the xy position drive result notification
    await rvr.on_xy_position_drive_result_notify(
        handler=on_xy_position_drive_result_notify_handler
    )

    # Reset yaw
    await rvr.reset_yaw()

    # Reset the locator too
    await rvr.reset_locator_x_and_y()

    # Start by setting the control system timeout to 10 seconds, just to get it
    # out of the way.
    await rvr.set_custom_control_system_timeout(command_timeout=10000)

    print("Driving forward...")
    await rvr.drive_rc_si_units(
        linear_velocity=1,      # Valid velocity values are in the range of [-2..2] m/s
        yaw_angular_velocity=0, # RVR will spin at up to 624 degrees/s.  Values outside of [-624..624] will saturate internally.
        flags=0
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    print("Requesting a stop with default deceleration")

    # This will request a stop with default deceleration.
    # Control of the motors is handed off to the stop controller,
    # which linearly ramps down the velocity targets of both treads.
    await rvr.drive_stop()

    # Wait until we receive the notification that the robot has stopped.
    while not rvr_has_stopped_from_handler:
        await asyncio.sleep(0)

    # Now clear the flag
    rvr_has_stopped_from_handler = False

    # Pause for a second for visibility
    await asyncio.sleep(1)

    # Return to our starting position and orientation.
    await return_to_start()

    print("Driving forward...")
    await rvr.drive_rc_si_units(
        linear_velocity=1,
        yaw_angular_velocity=0,
        flags=0
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    print("Requesting a stop with gentle deceleration")
    # This will request a stop with slower than normal deceleration.
    # Control of the motors is handed off to the stop controller,
    # which linearly ramps down the velocity targets of both treads.
    await rvr.drive_stop_custom_decel(
        deceleration_rate=0.5 # Decelerate both treads toward 0 velocity at 0.5 m/s^2
    )

    # In addition to the notification, it is also possible to poll whether the robot
    # has come to a stop.
    # This time, instead of using the notification to determine that the robot has stopped
    # we'll poll the stop controller state to decide when to continue
    rvr_stopped_from_polling = False
    while not rvr_stopped_from_polling:
        response = await rvr.get_stop_controller_state()
        print(response)
        rvr_stopped_from_polling = response['stopped']
        await asyncio.sleep(0.2)    # Some delay here is required to avoid flooding the UART

    rvr_has_stopped_from_handler = False

    # Pause for a second for visibility
    await asyncio.sleep(1)

    # Return to our starting position and orientation.
    await return_to_start()

    print("Driving forward...")
    await rvr.drive_rc_si_units(
        linear_velocity=1,
        yaw_angular_velocity=0,
        flags=0
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    print("Requesting a stop with rapid deceleration")
    # This will request a stop with faster than normal deceleration.
    # Control of the motors is handed off to the stop controller,
    # which linearly ramps down the velocity targets of both treads.
    await rvr.drive_stop_custom_decel(
        deceleration_rate=10 # Decelerate both treads toward 0 velocity at 10 m/s^2
    )

    # Wait until we receive the notification that the robot has stopped.
    while not rvr_has_stopped_from_handler:
        await asyncio.sleep(0)

    # Politely restore the default timeout (2 seconds)
    await rvr.restore_default_control_system_timeout()

    await asyncio.sleep(1)

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
