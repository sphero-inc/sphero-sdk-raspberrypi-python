import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio

from sphero_sdk import DriveControlAsync
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchornous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object, and pass in a SerialAsyncDal object, which in turn takes a reference
# to the asynchronous program loop
rvr = AsyncSpheroRvr(
    dal = SerialAsyncDal(
        loop
    )
)

# Create drive helper object that let's us control the LEDs of RVR
driver = DriveControlAsync(rvr)

async def main():

    await rvr.wake()

    # Reset yaw such that the heading will be set compared to the direction RVR is currently facing
    await driver.reset_heading()

    # Turn right degrees and drive for 1.5 seconds
    await driver.roll_start(64, 90)
    await asyncio.sleep(1.5)

    # Turn left (relative to original heading) and stop
    await driver.roll_stop(270)


# Run event loop until the main function has completed
loop.run_until_complete(
        main()
    )

# Stop the event loop
loop.stop()
# Close the event loop
loop.close()
