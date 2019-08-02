import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program demonstrates how to use the echo command, which sends data to RVR and has RVR return
        the same data. Echo can be used to check to see if RVR is connected and awake.

    """
    await
    rvr.wake()

    response = await
    rvr.echo(255, 1)
    print(response)


loop.run_until_complete(
    asyncio.gather(
        main()
    )
)

loop.stop()
loop.close()
