import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def on_ir_message_received(infraredCode):
    print("received code: {}".format(infraredCode))

def main():
    """
    This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    RVR listens for messages and performs the action as defined by on_ir_message_received when a message is
    received.
    At the same time, RVR sends out IR messages of code 0x03 continuously.
    """
    rvr.wake()

    # Register handler to be called when message is received
    rvr.on_robot_to_robot_infrared_message_received_notify(handler=on_ir_message_received)

    # Listen for IR messages of code 0x01 for the max amount of time
    rvr.listen_for_robot_to_robot_infrared_message(0x01, 0xffffffff)

    # time.sleep(1)

    # Send IR msg with code 0x03 at maximum strength from the front, rear, left and right sensor respectively
    while True:
        rvr.send_robot_to_robot_infrared_message(0x03, 255, 255, 255, 255)
        print("Message sent")
        time.sleep(0.2)

main()