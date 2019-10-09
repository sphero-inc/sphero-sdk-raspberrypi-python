import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver


rvr = SpheroRvrObserver()


def infrared_message_received_handler(infrared_message):
    print('Infrared message response: ', infrared_message)


def main():
    """ This program sets up RVR to communicate with another robot, e.g. BOLT, capable of infrared communication.
    """

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        rvr.on_robot_to_robot_infrared_message_received_notify(handler=infrared_message_received_handler)

        rvr.enable_robot_infrared_message_notify(is_enabled=True)

        infrared_code = 3
        strength = 64

        for _ in range(20):
            rvr.send_infrared_message(
                infrared_code=infrared_code,
                front_strength=strength,
                left_strength=strength,
                right_strength=strength,
                rear_strength=strength
            )

            print('Infrared message sent with code: {0}'.format(infrared_code))

            time.sleep(2)

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.stop_robot_to_robot_infrared_broadcasting()

        # Delay to allow RVR issue command before closing
        time.sleep(.5)
        
        rvr.close()


if __name__ == '__main__':
    main()
