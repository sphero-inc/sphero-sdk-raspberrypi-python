import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()


def on_battery_voltage_state_change(state):
    print("Battery voltage state changed; new state: ", state)


def main():
    """ This program demonstrates how to enable battery state change notifications and how to set up
    a handler for such notifications.

    """
    rvr.wake()

    # Instruct RVR to report battery change events
    rvr.enable_battery_voltage_state_change_notify(is_enabled=True)

    # Register handler to be called when a battery state change occur
    rvr.on_battery_voltage_state_change_notify(on_battery_voltage_state_change)

    rvr.close()


main()
