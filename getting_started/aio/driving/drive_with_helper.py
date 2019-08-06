import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import DriveControlAsync
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchronous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object, and pass in a SerialAsyncDal object, which in turn takes a reference
# to the asynchronous program loop
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)

# Create drive helper object that let's us control the LEDs of RVR
driver = DriveControlAsync(rvr)


async def main():
    """ This program has RVR drive and turn using the helper functions defined in DriveControlAsync.

        Note:
            To have RVR drive, we call asyncio.sleep(...); if we did not have these calls, the program would
            go on and execute all statements and exit without the driving ever taking place.
    """
    await rvr.wake()

    # Set aiming lights
    await driver.aim_start()

    # Reset yaw such that the heading will be set compared to the direction RVR is currently facing
    await driver.reset_heading()

    # Drive forward at speed 64 for one second
    await driver.drive_forward_seconds(64, 0, 1)

    # Drive backwards at speed 64 for one second
    await driver.drive_backward_seconds(64, 0, 1)

    # Turn left
    await driver.turn_left_degrees(0, 90)

    # Turn of aiming lights
    await driver.aim_stop()


# Run event loop until the main function has completed
loop.run_until_complete(
    main()
)

# Stop the event loop
loop.stop()
# Close the event loop
loop.close()
