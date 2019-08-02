import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

# Get a reference to the asynchornous program loop
loop = asyncio.get_event_loop()

# Create an AsyncSpheroRvr object, and pass in a SerialAsyncDal object, which in turn takes a reference
# to the asynchronous program loop 
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """
    This program has RVR drive around in different directions using the function raw_motors.
    
    Note:
        To give RVR time to drive, we call asyncio.sleep(...); if we did not have these calls, the program would 
        go on and execute all the statements and exit without the driving ever taking place. 
    """
    await
    rvr.wake()

    # Drive straight for one second at speed 128
    await
    rvr.raw_motors(1, 128, 1, 128)
    await
    asyncio.sleep(1)

    # Drive backwards for one second at speed 64
    await
    rvr.raw_motors(2, 64, 2, 64)
    await
    asyncio.sleep(1)

    # Turn right
    await
    rvr.raw_motors(2, 128, 1, 128)
    await
    asyncio.sleep(1)

    # Drive forward for 1 second at speed 128
    await
    rvr.raw_motors(1, 128, 1, 128)
    await
    asyncio.sleep(1)

    # Stop RVR
    await
    rvr.raw_motors(0, 0, 0, 0)


# Run event loop until the main function has completed
loop.run_until_complete(
    main()
)

# Stop the event loop
loop.stop()
# Close the event loop
loop.close()
