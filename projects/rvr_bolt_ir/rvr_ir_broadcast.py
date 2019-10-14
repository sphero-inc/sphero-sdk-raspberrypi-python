import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import time
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()
green1 = [0, 255, 0]
green2 = [0, 128, 0]


def main():
    rvr.wake()
    time.sleep(2)
    rvr.start_robot_to_robot_infrared_broadcasting(far_code=1,near_code=0)

    try:
        while True:
            rvr.set_all_leds(0x3FFFFFFF, [color for i in range(10) for color in green1])
            time.sleep(1)
            rvr.set_all_leds(0x3FFFFFFF, [color for i in range(10) for color in green2])
            time.sleep(2)
    except KeyboardInterrupt:
        rvr.stop_robot_to_robot_infrared_broadcasting()
        time.sleep(.1)
        rvr.close()


if __name__ == "__main__":
    main()
