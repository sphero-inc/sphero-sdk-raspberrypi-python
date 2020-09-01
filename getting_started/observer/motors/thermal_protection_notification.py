import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver
from sphero_sdk import TemperatureSensorsEnum

rvr = SpheroRvrObserver()


def thermal_protection_handler(response):
    print('Motor thermal protection response:', response)


def main():
    """ This program demonstrates how to register a handler for a motor thermal protection notification, in the event
        RVR's motors are at risk of overheating.  In order to receive the notification, RVR's motors must be heavily
        used for an extended period.

        For visibility into the motor temperatures, they are printed to the console every minute.
    """
    try:
        printing_loop_counter=9;

        rvr.wake()

        rvr.enable_motor_thermal_protection_status_notify(is_enabled=True)

        rvr.on_motor_thermal_protection_status_notify(handler=thermal_protection_handler)

        # Give RVR time to wake up
        time.sleep(1)

        print('Press CTRL+C to stop this program anytime.')

        # Allow RVR to drive infinitely
        while True:
            rvr.drive_tank_normalized(
                left_velocity=127, # Valid linear velocity values are [-127..127]
                right_velocity=-127 # Valid linear velocity values are [-127..127]
            )

            time.sleep(1)

            printing_loop_counter += 1
            if(++printing_loop_counter>=10):
                # It's been 1 minute.  Zero the counter
                printing_loop_counter = 0

                # Query the temperature
                response = rvr.get_temperature(
                    id0=TemperatureSensorsEnum.left_motor_temperature.value,
                    id1=TemperatureSensorsEnum.right_motor_temperature.value
                )

                # 2 Decimal places are displayed only to make changes more visible.
                # Motor thermal modeling is not actually that precise in practice.
                print("L={0:.2f}C, R={1:.2f}C".format(response["temp0"], response["temp1"]))

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()