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

# Handler for the active controller stopped notification.
# After sending a stop command, your program can wait for
# this async to confirm that the robot has come to a stop
async def stopped_handler():
    print('RVR has stopped')


async def main():
    """ This program has RVR drive around using the normalized RC drive command.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    # Register the handler for the stopped notification
    await rvr.on_robot_has_stopped_notify(handler=stopped_handler)

    await rvr.reset_yaw()

    print("sending drive command")

    await rvr.drive_rc_normalized(
        linear_velocity=20,  # Valid linear velocity values are -127..127
        yaw_angular_velocity=0,  # Valid angular velocity values are -127..127
        flags=0
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(2)

    # Continue driving forward, while turning left
    await rvr.drive_rc_normalized(
        linear_velocity=15,         # Valid linear velocity values are -127..127
        yaw_angular_velocity=20,    # Valid angular velocity values are -127..127
        flags=0
    )

    # Delay to allow RVR to turn
    await asyncio.sleep(1)

    # Drive in new forward direction
    await rvr.drive_rc_normalized(
        linear_velocity=20,  # Valid linear velocity values are -127..127
        yaw_angular_velocity=0,  # Valid angular velocity values are -127..127
        flags=0
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(2)

    print("sending stop command")

    # Stop driving, with deceleration rate of 2 m/s^2
    await rvr.drive_stop(2.0)

    # Delay to allow RVR to stop
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
