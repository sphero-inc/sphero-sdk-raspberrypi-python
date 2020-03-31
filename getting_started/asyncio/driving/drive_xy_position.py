import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import RawMotorModesEnum


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

# Flag used to wait for move completion
move_completed=False

async def test_handler(response):
    global move_completed

    move_completed=True
    print("Move completed")

async def drive_to_position_wait_to_complete(yaw_angle,x,y,linear_velocity,flags):
    global move_completed

    print("Driving to ({0},{1}) at {2} degrees".format(x,y,yaw_angle))

    # Clear the completion flag
    move_completed=False

    await rvr.drive_to_position_si(
        yaw_angle=yaw_angle,
        x=x,
        y=y,
        linear_velocity=linear_velocity,
        flags=flags,
    )

    while (move_completed==False):
        await asyncio.sleep(.5)

async def main():
    """ This program has RVR drive in a square using the (x,y) coordinate drive system.
    """
    global move_completed

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Reset the yaw and locator
    await rvr.reset_yaw()
    await asyncio.sleep(.1)
    await rvr.reset_locator_x_and_y()
    await asyncio.sleep(.1)

    print("Registering async")

    #await rvr.enable_motor_fault_notify(is_enabled=True)

    # Register for the async on completion of the drive operation
    # await rvr.on_xy_position_drive_result_notify(handler=on_position_drive_done)
    # switched the CID to motor fault as a crazy test
    await rvr.on_motor_fault_notify(handler=test_handler)

    await drive_to_position_wait_to_complete(
        yaw_angle=-90,
        x=0,
        y=0.2,
        linear_velocity=2,
        flags=0,
    )

    await drive_to_position_wait_to_complete(
        yaw_angle=-180,
        x=0.2,
        y=0.2,
        linear_velocity=2,
        flags=0,
    )

    await drive_to_position_wait_to_complete(
        yaw_angle=90,
        x=0.2,
        y=0,
        linear_velocity=2,
        flags=0,
    )

    await drive_to_position_wait_to_complete(
        yaw_angle=0,
        x=0,
        y=0,
        linear_velocity=2,
        flags=0,
    )

    await asyncio.sleep(5)


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
