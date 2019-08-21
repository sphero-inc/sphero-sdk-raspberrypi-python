import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))


def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.

        To try this out, write a script for your other robot that a) broadcasts on the corresponding
        channel that RVR is set to listen to [in this case channel 0] and b) listens on the channel which
        RVR sends messages on [in this case channel 3]
    """
    rvr.wake()

    # Give RVR time to wake up
    time.sleep(2)

    enabled = True
    rvr.enable_robot_infrared_message_notify(enabled)

    rvr.on_robot_to_robot_infrared_message_received_notify(on_ir_message_received)

    # Send infrared message with code 3 at maximum strength from the front, rear, left and right sensor respectively
    infrared_code = 3
    strength = 64

    for _ in range(20):
        rvr.send_infrared_message(infrared_code, strength, strength, strength, strength)
        print("message sent with code {}".format(infrared_code))
        time.sleep(0.2)

    rvr.close()


main()
