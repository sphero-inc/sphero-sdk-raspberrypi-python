import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def on_about_to_enter_soft_sleep():
    print("RVR is about to enter soft sleep...")
    # Here we could issue a command to RVR, e.g. wake() such that the sleep timer is reset
    # and RVR does not go to sleep


def on_entered_soft_sleep():
    print("RVR entered soft sleep...")


def main():
    """ This program demonstrates how to register handlers for a) the event received 10 seconds
    before RVR will enter soft sleep unless some new command is issued and b) the event received
    when RVR does enter soft sleep.

    Note that these notifications are received without the need to enable them on the robot.

    """
    rvr.wake()

    rvr.on_will_sleep_notify(on_about_to_enter_soft_sleep)

    rvr.on_did_sleep_notify(on_entered_soft_sleep)

    # Sleep for 310 seconds such that we see the aforementioned events have time to occur
    time.sleep(310)

    rvr.close()


main()
