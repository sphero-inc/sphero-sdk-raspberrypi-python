import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import BatteryVoltageStatesEnum as VoltageStates


rvr = SpheroRvrObserver()


def battery_percentage_handler(battery_percentage):
    print('Battery percentage: ', battery_percentage)


def battery_voltage_handler(battery_voltage_state):
    print('Voltage state: ', battery_voltage_state)

    state_info = '[{}, {}, {}, {}]'.format(
        '{}: {}'.format(VoltageStates.unknown.name, VoltageStates.unknown.value),
        '{}: {}'.format(VoltageStates.ok.name, VoltageStates.ok.value),
        '{}: {}'.format(VoltageStates.low.name, VoltageStates.low.value),
        '{}: {}'.format(VoltageStates.critical.name, VoltageStates.critical.value)
    )
    print('Voltage states: ', state_info)


def main():
    """ This program demonstrates how to retrieve the battery state of RVR.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.get_battery_percentage(handler=battery_percentage_handler)

        # Sleep for one second such that RVR has time to send data back
        time.sleep(1)

        rvr.get_battery_voltage_state(handler=battery_voltage_handler)

        # Sleep for one second such that RVR has time to send data back
        time.sleep(1)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
