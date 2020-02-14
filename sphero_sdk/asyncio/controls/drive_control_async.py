#!/usr/bin/env python

import asyncio
from datetime import datetime

from sphero_sdk import LedControlAsync
from sphero_sdk.common.enums.rvr_led_groups_enum import RvrLedGroups
from sphero_sdk.common.enums.colors_enums import Colors


class DriveControlAsync:
    """DriveControlAsync is a class that abstracts the driving process so that the user doesn't have to
        use the run_raw_motors command to drive RVR.

        Args:
            rvr (SpheroRvrAsync): Instance of an AsyncSpheroRvr containing an event loop


        Returns:


        """

    __drive_no_flag = 0x00
    __drive_reverse_flag = 0x01

    def __init__(self, rvr):
        if rvr is None:
            raise TypeError('ERROR: PASS IN A RVR OBJECT')

        self.__rvr = rvr

        self.__led_control = LedControlAsync(self.__rvr)    # TODO: eventually call self.__rvr.led_control

        return

    async def reset_heading(self):
        """reset_heading resets the heading of the RVR

        """

        await self.__rvr.reset_yaw()

        return

    async def drive_backward_seconds(self, speed=0, heading=0, time_to_drive=1):
        """drive_backward_seconds drives the RVR backward with a specified heading and speed for some number of seconds

        Args:
            speed (uint8): integer between 0 and 255
            heading (int): integer between 0 and 359
            time_to_drive (int): number of seconds to drive

        """

        await self.__timed_drive(speed, heading, DriveControlAsync.__drive_reverse_flag, time_to_drive)

        return

    async def drive_forward_seconds(self, speed=0, heading=0, time_to_drive=1):
        """drive_forward_seconds drives the RVR forward with a specified heading and speed for some number of seconds

        Args:
            speed (uint8): integer between 0 and 255
            heading (int): integer between 0 and 359
            time_to_drive (int): number of seconds to drive

        """

        await self.__timed_drive(speed, heading, DriveControlAsync.__drive_no_flag, time_to_drive)

        return

    async def turn_left_degrees(self, heading, amount=90):
        """turn_left_degrees rotates the RVR counter-clockwise some number of degrees starting at a given heading. The
        rotation will default to 90 degrees if none is provided

        Args:
            heading (int): heading from where the turn will start
            amount (int): number of degrees to turn

        """
        new_heading = (heading - amount) % 360
        await self.__rvr.drive_with_heading(0, new_heading, DriveControlAsync.__drive_no_flag)
        await asyncio.sleep(0.1)

        return

    async def turn_right_degrees(self, heading, amount=90):
        """turn_right_degrees rotates the RVR clockwise some number of degrees starting at a given heading. The
        rotation will default to 90 degrees if none is provided

        Args:
            heading (int): heading from where the turn will start (number between 0 and 359)
            amount (int): number of degrees to turn

        """

        await self.__rvr.drive_with_heading(0, heading + amount, DriveControlAsync.__drive_no_flag)
        await asyncio.sleep(0.1)

        return

    async def roll_start(self, speed, heading):
        """roll_start rolls the RVR forward at a specified heading and speed

        Args:
            speed (uint8): integer between 0 and 255
            heading (int): integer between 0 and 359

        """

        flags = 0

        while heading < 0:
            heading += 360

        if speed < 0:
            flags = flags | DriveControlAsync.__drive_reverse_flag

        speed = abs(speed)
        if speed > 255:
            speed = 255

        heading = heading % 360

        await self.__rvr.drive_with_heading(speed, heading, flags)

        return

    async def roll_stop(self, heading):
        """roll_stop stops the RVR and faces it towards a specified heading

        Args:
            heading (int): integer between 0 and 359

        """

        await self.roll_start(0, heading)

        return

    async def set_heading(self, heading):
        """set_heading faces the RVR towards a specified heading

        Args:
            heading (int): integer between 0 and 359

        """

        await self.roll_stop(heading)

        return

    async def aim_start(self):
        """aim_start sets rear lights on RVR blue indicating the aiming process is starting

        """

        await self.__led_control.set_multiple_leds_with_enums(
            [RvrLedGroups.brakelight_left, RvrLedGroups.brakelight_right],
            [Colors.blue, Colors.blue]
        )

        return

    async def aim_stop(self):
        """aim_stop turns the rear lights off and resets the heading of the RVR

        """
        # TODO: Add function for idling lights in the SDK
        await self.reset_heading()

        await self.__led_control.set_multiple_leds_with_enums(
            [RvrLedGroups.brakelight_left, RvrLedGroups.brakelight_right],
            [Colors.off, Colors.off]
        )

        return

    async def __timed_drive(self, speed, heading, flags, time_to_drive):
        timer_start = DriveControlAsync.__get_timer_seconds()

        while DriveControlAsync.__get_timer_seconds() <= timer_start + time_to_drive:
            await self.__rvr.drive_with_heading(speed, heading, flags)
            await asyncio.sleep(0.1)

        await self.__rvr.drive_with_heading(0, heading, flags)

        return

    @staticmethod
    def __get_timer_seconds():
        # isolate characters 6 through 9 to obtain seconds down to tenth of second ([6:10] is exclusive on upper bound)
        seconds = float(str(datetime.now().time())[6:10])

        return seconds
