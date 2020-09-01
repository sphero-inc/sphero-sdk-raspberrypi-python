import os
import sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()

# Flag used to wait for move completion
move_completed = False

# Handler for completion of XY position drive moves
def on_xy_position_drive_result_notify_handler(response):
    global move_completed

    move_completed = True
    print('Move completed, response:', response)


# This wrapper function implements a simple way to send a drive to position command
# and then wait for the move to complete
def drive_to_position_wait_to_complete(yaw_angle,x,y,linear_speed,flags):
    global move_completed

    print("Driving to ({0},{1}) at {2} degrees".format(x,y,yaw_angle))

    # Clear the completion flag
    move_completed = False

    # Send the drive command, passing the wrapper function parameters into the matching
    # parameters in rvr.drive_to_position_normalized (which sends the actual drive command)
    rvr.drive_to_position_si(
        yaw_angle=yaw_angle,              # 0 degrees is straight ahead, +CCW (Following the right hand rule)
        x=x,                              # Target position X coordinate in meters
        y=y,                              # Target position Y coordinate in meters
        linear_speed=linear_speed,        # Max speed in transit to target, in m/s.  Max value is 1.555 m/s
        flags=flags,                      # Option flags
    )

    # Wait to complete the move.  Note: In a real project, a timeout mechanism
    # should be here to prevent the script from getting caught in an infinite loop
    while not move_completed:
        time.sleep(0)


def main():
    """ This program has RVR drive in a square using the (x,y) coordinate drive system.
    """

    try:
        global move_completed

        # Square parameters
        side_length = 0.5   # 0.5 m
        max_speed = 2       # 2 m/s

        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Reset the yaw and locator.
        rvr.reset_yaw()
        time.sleep(.1)
        rvr.reset_locator_x_and_y()
        time.sleep(.1)

        print("Registering async")

        # Register for the on completion of the drive operation
        # rvr.on_xy_position_drive_result_notify(handler=on_position_drive_done)
        # switched the CID to motor fault as a crazy test
        rvr.on_xy_position_drive_result_notify(handler=on_xy_position_drive_result_notify_handler)

        drive_to_position_wait_to_complete(
            yaw_angle=-90,
            x=0,
            y=side_length,
            linear_speed=max_speed,
            flags=0,
        )

        drive_to_position_wait_to_complete(
            yaw_angle=-180,
            x=side_length,
            y=side_length,
            linear_speed=max_speed,
            flags=0,
        )

        drive_to_position_wait_to_complete(
            yaw_angle=90,
            x=side_length,
            y=0,
            linear_speed=max_speed,
            flags=0,
        )

        drive_to_position_wait_to_complete(
            yaw_angle=0,
            x=0,
            y=0,
            linear_speed=max_speed,
            flags=0,
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

    finally:
        rvr.close()


if __name__ == '__main__':
    main()
