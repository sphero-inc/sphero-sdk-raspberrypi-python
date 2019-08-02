import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()


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

    # Register handler to be called when message is received
    rvr.on_robot_to_robot_infrared_message_received_notify(handler=on_ir_message_received)

    # Listen for messages at channel 0 for the maximum amount of time possible
    # Note: The channel is given as a bit mask
    # In this case, we want to listen to channel 0, so the first bit is set to 1
    infrared_code = 0x01
    listen_duration = 0xffffffff
    rvr.listen_for_robot_to_robot_infrared_message(infrared_code, listen_duration)

    # Send infrared message with code 3 at maximum strength from the front, rear, left and right sensor respectively
    infrared_code = 3
    strength = 64

    for _ in range(20):
        rvr.send_robot_to_robot_infrared_message(infrared_code, strength, strength, strength, strength)
        print("message sent with code {}".format(infrared_code))
        time.sleep(0.2)

    rvr.close()


main()
