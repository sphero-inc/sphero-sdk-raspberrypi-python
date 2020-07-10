import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrTargets


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """
    """
    await rvr.generate_api_error(
        error=1,
        target=SpheroRvrTargets.primary.value
    )


if __name__ == '__main__':
    try:
        asyncio.ensure_future(main())
        loop.run_forever()

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
