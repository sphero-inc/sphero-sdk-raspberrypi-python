import os
import sys
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def battery_percentage_handler(battery_percentage):
    print('Battery percentage: ', battery_percentage)


def battery_voltage_handler(battery_voltage_state):
    print('Voltage state: ', battery_voltage_state)

    state_info = {
        0: 'Unknown',
        1: 'OK',
        2: 'Low',
        3: 'Critical'
    }  # TODO: are these autogen'd and can they be referenced instead?
    print('Voltage states: ', state_info)


def main():
    """ This program demonstrates how to retrieve the battery state of RVR.
    """

    rvr.wake()

    # give RVR time to wake up
    time.sleep(2)

    rvr.get_battery_percentage(handler=battery_percentage_handler)

    # sleep for one second such that RVR has time to send data back
    time.sleep(1)

    rvr.get_battery_voltage_state(handler=battery_voltage_handler)

    # sleep for one second such that RVR has time to send data back
    time.sleep(1)

    rvr.close()


if __name__ == '__main__':
    main()
