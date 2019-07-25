import asyncio
import time

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()
rvr = AsyncSpheroRvr(dal=SerialAsyncDal(loop=loop))


async def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))
    pass


async def main():
    await rvr.wake()
    await rvr.on_robot_to_robot_infrared_message_received_notify(handler=on_ir_message_received)
    await rvr.listen_for_robot_to_robot_infrared_message(0x01,0xffffffff)


try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()

time.sleep(1)
loop.close()
