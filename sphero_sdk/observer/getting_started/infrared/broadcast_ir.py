import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def main():
    """
    Place your BOLT or other robot that has a support for infrared following. Make sure to set your other robot
    to follow the channels specified below. Upon running this program RVR should drive forward and the other robot
    follow it.
    Returns:

    """
    rvr.wake()

    rvr.start_robot_to_robot_infrared_broadcasting(0x00, 0x01)

    rvr.raw_motors(1, 128, 1, 128)
    time.sleep(1)

    rvr.stop_robot_to_robot_infrared_broadcasting()

main()