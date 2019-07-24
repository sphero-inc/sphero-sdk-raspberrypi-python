import sys
sys.path.append('/home/pi/raspberry-pi-python')

import asyncio

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

async def drive_with_heading(speed, heading, flags):
    await rvr.drive_with_heading(speed, heading, flags)
            
async def stop_raw_motors():
    await rvr.raw_motors(0,0,0,0)


async def main():
    """
    Note:
        To give RVR time to drive, we call asyncio.sleep(...); if we did not have these calls, the program would 
        go on and execute all the statements and exit without the driving ever taking place. 
    """
    print("starting...")
    # Drive straight for one second at speed 128
    await drive_with_heading(128, 0, 0)
    await asyncio.sleep(1) 
    print("drive forward")
    # Drive backwards for one second at speed 128
    await drive_with_heading(128, 180, 0)
    await asyncio.sleep(1)
    # Turn right
    # Note: To accomplish the turn, the left motor is set to go backwards (left_mode is set to 2)
    # and the right motor is set to go forward (right_mode is set to 1)
    await drive_with_heading(128, 90, 0)
    await asyncio.sleep(0.5)
    # Stop RVR 
    await stop_raw_motors()

# Run event loop until the main function has completed
loop.run_until_complete(
        main()
    )

# Stop the event loop
loop.stop()
# Close the event loop
loop.close()
