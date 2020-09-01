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

    await rvr.drive_rc_si_units(
        linear_velocity=.3,     # Valid velocity values are in the range of [-2..2] m/s
        yaw_angular_velocity=0, # RVR will spin at up to 624 degrees/s.  Values outside of [-624..624] will saturate internally.
        flags=0
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    # The control system timeout can be modified to keep a command running longer
    # than the default 2 seconds.  This remains in effect until changed back,
    # or until a reboot occurs. Note that this is in milliseconds.
    await rvr.set_custom_control_system_timeout(command_timeout=20000)

    # Continue driving forward, while turning left
    await rvr.drive_rc_si_units(
        linear_velocity=.1,
        yaw_angular_velocity=20,
        flags=0
    )

    # Delay to allow RVR to drive
    await asyncio.sleep(18)         # Oh look, there'll be 2 seconds of driving to go!

    print("sending stop command")

    # Stop early, with a custom deceleration rate of 2 m/s^2.
    await rvr.drive_stop(2.0)

    # Restore the default control system timeout to keep things more normal after this.
    await rvr.restore_default_control_system_timeout()

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
