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

# Flag used to indicate that calibration is complete
calibration_completed = False

# Initial yaw offset to magnetic North
yaw_north = 0

# Handler for completion of calibration
async def on_calibration_complete_notify_handler(response):
    global calibration_completed
    global yaw_north

    print('Calibration complete, response:', response)
    yaw_north = response['yaw_north_direction']
    calibration_completed = True
    


async def main():
    """ This program demonstrates the magnetometer calibration to find north.
    """

    global calibration_completed
    global yaw_north

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Register for the async on completion of calibration
    await rvr.on_magnetometer_calibration_complete_notify(handler=on_calibration_complete_notify_handler)

    # Begin calibration
    print('Begin magnetometer calibration to find North...')
    await rvr.magnetometer_calibrate_to_north()

    # Wait to complete the calibration.  Note: In a real project, a timeout mechanism
    # should be here to prevent the script from getting caught in an infinite loop
    while not calibration_completed:
        await asyncio.sleep(.1)

    print('Turning to face north')

    # Turn to face north
    await rvr.drive_with_yaw_normalized(
        yaw_angle=yaw_north, 
        linear_velocity=0
    )

    # Leave some time for it to complete the move
    await asyncio.sleep(2)

    # Reset yaw to zero.  After this, zero heading will be magnetic north
    await rvr.reset_yaw()

    print('Turning to face east')

    # You can now drive along compass headings as follows (adjust linear velocity to drive forward)
    await rvr.drive_with_heading(
        speed = 0,  # This is normalized 0-255.  0 will cause RVR to turn in place
        heading=90, # This is the compass heading
        flags=0     # Just leave this at zero to drive forward
    )

    # Allow some time for the move to complete before we end our script
    await asyncio.sleep(2)

    await rvr.close();


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            asyncio.gather(
                rvr.disable_notifications_and_active_commands(),
                rvr.close()
            )
        )

    finally:
        if loop.is_running():
            loop.close()
