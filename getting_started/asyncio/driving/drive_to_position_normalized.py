import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

# Flag used to wait for move completion
move_completed = False

# Handler for completion of XY position drive moves
async def on_xy_position_drive_result_notify_handler(response):
    global move_completed

    move_completed = True
    print('Move completed, response:', response)


# This wrapper function implements a simple way to send a drive to position command
# and then wait for the move to complete
async def drive_to_position_wait_to_complete(yaw_angle,x,y,linear_speed,flags):
    global move_completed

    print("Driving to ({0},{1}) at {2} degrees".format(x,y,yaw_angle))

    # Clear the completion flag
    move_completed = False

    # Send the drive command, passing the wrapper function parameters into the matching
    # parameters in rvr.drive_to_position_normalized (which sends the actual drive command)
    await rvr.drive_to_position_normalized(
        yaw_angle=yaw_angle,             # 0 degrees is straight ahead, +CCW (Following the right hand rule)
        x=x,                             # Target position X coordinate in meters
        y=y,                             # Target position Y coordinate in meters
        linear_speed=linear_speed,       # Max speed in transit to target.  Normalized in the range [0..127]
        flags=flags,                     # Option flags
    )

    # Wait to complete the move.  Note: In a real project, a timeout mechanism
    # should be here to prevent the script from getting caught in an infinite loop
    while not move_completed:
        await asyncio.sleep(0)


async def main():
    """ This program has RVR drive in a square using the (x,y) coordinate drive system.
    """
    global move_completed

    # Square parameters
    side_length = 0.5  # 0.5 m
    max_speed = 64  # 50% of full speed

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Reset the yaw and locator.
    await rvr.reset_yaw()
    await asyncio.sleep(.1)
    await rvr.reset_locator_x_and_y()
    await asyncio.sleep(.1)

    print("Registering async")

    # Register for the async on completion of the drive operation
    await rvr.on_xy_position_drive_result_notify(handler=on_xy_position_drive_result_notify_handler)

    await drive_to_position_wait_to_complete(
        yaw_angle=-90,
        x=0,
        y=side_length,
        linear_speed=max_speed,
        flags=0,
    )

    await drive_to_position_wait_to_complete(
        yaw_angle=-180,
        x=side_length,
        y=side_length,
        linear_speed=max_speed,
        flags=0,
    )

    await drive_to_position_wait_to_complete(
        yaw_angle=90,
        x=side_length,
        y=0,
        linear_speed=max_speed,
        flags=0,
    )

    await drive_to_position_wait_to_complete(
        yaw_angle=0,
        x=0,
        y=0,
        linear_speed=max_speed,
        flags=0,
    )

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
