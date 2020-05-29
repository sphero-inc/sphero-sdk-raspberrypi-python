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

# Handler for completion of calibration 
async def on_calibration_complete_notify_handler(response):
    global calibration_completed

    print('Calibration complete, response:', response)
    calibration_completed = True 


async def main():
    """ This program demonstrates the magnetometer calibration to find north. 
    """

    global calibration_completed

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
    while (calibration_completed == False):
        await asyncio.sleep(0)

    await rvr.close();
    

if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.disable_notifications_and_active_commands(),
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
