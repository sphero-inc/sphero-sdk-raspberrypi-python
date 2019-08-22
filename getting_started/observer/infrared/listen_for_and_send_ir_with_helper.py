# InfraredControlObserver.listen_for_infrared_message(...) has problems

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import InfraredControlObserver
from sphero_sdk import InfraredCodes

rvr = SpheroRvrObserver()

infrared_controller = InfraredControlObserver(rvr)


def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))


def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.

       To try this out, write a script for your other robot that a) broadcasts on any channel and b) listens on the
       channel which RVR sends messages on [in this case channel 0, 1, 2, and 3]
    """
    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    infrared_controller.listen_for_infrared_message(on_ir_message_received)

    codes = [InfraredCodes.zero, InfraredCodes.one, InfraredCodes.two, InfraredCodes.three]
    for _ in range(20):
        infrared_controller.send_infrared_messages(codes, strength=64)
        print("message sent with codes {}".format([code.value for code in codes]))
        time.sleep(0.2)

    rvr.close()


main()
