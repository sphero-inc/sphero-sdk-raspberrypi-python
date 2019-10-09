import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def battery_voltage_state_change_handler(battery_voltage_state):
    print('Battery voltage state: ', battery_voltage_state)


def main():
    """ This program demonstrates how to enable battery state change notifications.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.on_battery_voltage_state_change_notify(handler=battery_voltage_state_change_handler)
        rvr.enable_battery_voltage_state_change_notify(is_enabled=True)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
