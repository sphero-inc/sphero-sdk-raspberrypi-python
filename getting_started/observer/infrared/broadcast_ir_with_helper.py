# No response from BOLT
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import InfraredControlObserver
from sphero_sdk import InfraredCodes

rvr = SpheroRvrObserver()


infrared_controller = InfraredControlObserver(rvr)


def main():
    """ This program has another robot capable of infrared communication, e.g. BOLT, follow RVR.

        To try this out, write a script for your other robot that has it follow on the corresponding channel
        that RVR broadcasts on [in this case channel 0 and 1].
        Place your other robot behind RVR and run its script.
        Upon running this program RVR drives forward and the other robot follows it.
    """
    rvr.wake()
    time.sleep(2)

    # Broadcast on channels 0, 1, 2, and 3. We specify the channels with the InfraredCodes enumeration
    near_code = InfraredCodes.zero
    far_code = InfraredCodes.one
    infrared_controller.start_infrared_broadcasting(far_code, near_code)

    rvr.raw_motors(1, 64, 1, 64)
    time.sleep(2)

    infrared_controller.stop_infrared_broadcasting()

    rvr.close()


main()