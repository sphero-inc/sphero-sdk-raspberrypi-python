import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import ControlSystemTypesEnum
from sphero_sdk import ControlSystemIdsEnum


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program demonstrates setting and getting the default controller
        for a given control system type.  This allows you to select the
        underlying controller that handles driving.

        A "control system type" is a category of driving control style.  For
        example, RC style takes a target speed and rotational velocity, just
        like an RC car.  Another example is tank drive, which takes individual
        wheel speeds for RVR's left and right treads.

        A "controller" is the underlying mechanism that handles a particular
        control system type.  Selecting the controller allows you to choose
        how RVR handles different situations.  For example, RC driving provides
        two controller options: (1) the "slew mode" which uses a slewed target
        yaw to achieve RVR's rotation, and (2) the "rate mode" which uses
        rotation rate measured directly from the gyroscope.  These controllers
        differ in how they handle obstacles.  Slew mode is "smart" about
        heading.  If RVR encounters an uneven surface or is bumped while
        driving, the slew mode controller will actively adjust RVR's rotation
        to compensate, fighting to maintain its intended, rotating target yaw.
        The "rate mode" is more similar to a traditional RC car.  An uneven
        surface or bump will more directly affect the driving direction. In
        this example, Sphero recommends "slew mode" for programmed maneuvers
        and "rate mode" for a more natural driving experience.

        An important note: a new controller selection takes effect when RVR is
        stopped, so you must issue a stop command to change.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    await rvr.reset_yaw()

    # Get the default controllers for stop and RC
    control_system_type = ControlSystemTypesEnum.control_system_type_stop
    response = await rvr.get_default_control_system_for_type(control_system_type = control_system_type)
    print(response)
    controller_id = ControlSystemIdsEnum(response['controller_id'])
    print('Default controller for {} is {}'.format(control_system_type.name, controller_id.name))

    control_system_type = ControlSystemTypesEnum.control_system_type_rc_drive
    response = await rvr.get_default_control_system_for_type(control_system_type = control_system_type)
    controller_id = ControlSystemIdsEnum(response['controller_id'])
    print('Default controller for {} is {}'.format(control_system_type.name, controller_id.name))


    # We are currently stopped. Get the currently active control system.
    print('Getting current control system...')
    response = await rvr.get_active_control_system_id()
    controller_id = ControlSystemIdsEnum(response['controller_id'])
    print('Active controller: {}'.format(controller_id.name))


    # Drive a bit with RC and check the active control system
    print('Driving with RC...')
    await rvr.drive_rc_si_units(linear_velocity=1, yaw_angular_velocity=0, flags=0 )
    response = await rvr.get_active_control_system_id()
    controller_id = ControlSystemIdsEnum(response['controller_id'])
    print('Active controller: {}'.format(controller_id.name))

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    # Stop the robot
    print('Stopping...')
    await rvr.drive_stop()

    # We don't actually need it to stop, so no delay here.  We just needed the RC drive command to be inactive

    # Set the default control system for RC and drive some more
    control_system_type = ControlSystemTypesEnum.control_system_type_rc_drive
    controller_id = ControlSystemIdsEnum.rc_drive_slew_mode
    print('Setting default control system for RC drive to {}'.format(controller_id.name))
    await rvr.set_default_control_system_for_type(control_system_type = control_system_type, controller_id = controller_id)

    print('Driving with RC...')
    await rvr.drive_rc_si_units(linear_velocity=1, yaw_angular_velocity=0, flags=0 )
    response = await rvr.get_active_control_system_id()
    controller_id = ControlSystemIdsEnum(response['controller_id'])
    print('Active controller: {}'.format(controller_id.name))

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    # Stop the robot
    print('Stopping...')
    await rvr.drive_stop()

    # Restore initial default control systems
    print('Restore initial default control systems')
    await rvr.restore_initial_default_control_systems()

    print('Driving with RC...')
    await rvr.drive_rc_si_units(linear_velocity=1, yaw_angular_velocity=0, flags=0 )
    response = await rvr.get_active_control_system_id()
    controller_id = ControlSystemIdsEnum(response['controller_id'])
    print('Active controller: {}'.format(controller_id.name))

    # Delay to allow RVR to drive
    await asyncio.sleep(1)

    await rvr.close()


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()
