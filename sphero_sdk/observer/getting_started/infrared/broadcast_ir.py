import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def main():
    """
        This program has another robot capable of infrared communication, e.g. BOLT, follow RVR.

        To try this out, write a script for your other robot that has it follow on the corresponding channel
        that RVR broadcasts on [in this case channel 0 and 1].
        Place your other robot behind RVR and run its script.
        Upon running this program RVR drives forward and the other robot follows it.
    """
    rvr.wake()

    rvr.start_robot_to_robot_infrared_broadcasting(0x00, 0x01)

    rvr.raw_motors(1, 128, 1, 128)
    time.sleep(1)

    rvr.stop_robot_to_robot_infrared_broadcasting()

main()