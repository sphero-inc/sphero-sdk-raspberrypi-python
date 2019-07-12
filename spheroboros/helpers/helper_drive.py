import sys

sys.path.append('/home/pi/raspberry-pi')

import asyncio
from spheroboros import AsyncSpheroRvr
from spheroboros import SerialAsyncDal
from spheroboros.helpers.helper_leds import HelperLEDs
from spheroboros.helpers.helper_colors_enum import Color
from spheroboros.helpers.helper_lights_enum import RvrLeds
from datetime import datetime


class DriveHelper:
    """DriveHelper is a class that abstracts the driving process so that the user doesn't have to
        use the run_raw_motors command to drive RVR.

        Args:
            rvr (AsyncSpheroRvr): Instance of an AsyncSpheroRvr containing an event loop


        Returns:


        """

    def __init__(self, rvr):
        self.__rvr = rvr
        self.__is_boosting = False
        self.__drive_reverse = 1
        self.__drive_boost = 2
        self.__light_manager = HelperLEDs(self.__rvr)
        return

    @property
    def is_boosting(self):
        return self.__is_boosting

    @is_boosting.setter
    def is_boosting(self, set_boost):
        self.__is_boosting = set_boost
        return

    async def reset_heading(self):
        """reset_heading resets the heading of the RVR

        Returns:

        """
        await self.__rvr.reset_yaw()
        return

    async def stop_raw_motors(self):
        """stop_raw_motors stops the RVR

        Returns:

        """
        await self.__rvr.drive_with_heading(0, 0, 0)
        return

    async def drive_backward_seconds(self, speed=0, heading=0, time_to_drive=1):
        """drive_backward_seconds drives the RVR backward with a specified heading and speed for some number of seconds

        Args:
            speed (int): integer between 0 and 255
            heading (int): integer between 0 and 359
            time_to_drive (int): number of seconds to drive

        Returns:

        """
        await self.__timed_drive(heading, speed, 1, time_to_drive)
        return

    async def drive_forward_seconds(self, speed=0, heading=0, time_to_drive=1):
        """drive_forward_seconds drives the RVR forward with a specified heading and speed for some number of seconds

        Args:
            speed (int): integer between 0 and 255
            heading (int): integer between 0 and 359
            time_to_drive (int): number of seconds to drive

        Returns:

        """
        await self.__timed_drive(heading, speed, 0, time_to_drive)
        return

    async def turn_left_degrees(self, heading, amount=90):
        """turn_left_degrees rotates the RVR counter-clockwise some number of degrees starting at a given heading. The
        rotation will default to 90 degrees if none is provided

        Args:
            heading (int): heading from where the turn will start
            amount (int): number of degrees to turn

        Returns:

        """

        await self.__rvr.drive_with_heading(0, heading-amount, 0)
        await asyncio.sleep(0.1)
        return

    async def turn_right_degrees(self, heading, amount=90):
        """turn_right_degrees rotates the RVR clockwise some number of degrees starting at a given heading. The
        rotation will default to 90 degrees if none is provided

        Args:
            heading (int): heading from where the turn will start (number between 0 and 359)
            amount (int): number of degrees to turn

        Returns:

        """

        await self.__rvr.drive_with_heading(0, heading+amount, 0)
        await asyncio.sleep(0.1)
        return

    async def roll_start(self, speed, heading):
        """roll_start rolls the RVR forward at a specified heading and speed

        Args:
            speed (int): integer between 0 and 255
            heading (int): integer between 0 and 359

        Returns:

        """
        flag = 0
        if self.is_boosting:
            flag = flag | self.__drive_boost

        while heading < 0:
            heading += 360

        if speed < 0:
            flag = flag | self.__drive_reverse
            heading += 180

        speed = abs(speed)
        if speed > 255:
            speed = 255

        await self.__rvr.drive_with_heading(speed, heading % 360, flag)
        return

    async def roll_stop(self, heading):
        """roll_stop stops the RVR and faces it towards a specified heading

        Args:
            heading (int): integer between 0 and 359

        Returns:

        """
        await self.roll_start(heading, 0)
        return

    async def set_heading(self, heading):
        """set_heading faces the RVR towards a specified heading

        Args:
            heading (int): integer between 0 and 359

        Returns:

        """
        await self.roll_stop(heading)
        return

    async def aim_start(self):
        """aim_start sets rear lights on RVR blue indicating the aiming process is starting

        Returns:

        """
        await self.__light_manager.turn_lights_off()
        await self.__light_manager.set_multiple_lights_enum([RvrLeds.rear_1, RvrLeds.rear_2], [Color.blue, Color.blue])
        return

    async def aim_stop(self):
        """aim_stop turns the rear lights off and resets the heading of the RVR

        Returns:

        """
        # TODO: Add function to idling lights in the SDK
        await self.reset_heading()
        await self.__light_manager.turn_lights_off()
        return

    @staticmethod
    def __update_timer(timer_start, timer):
        # isolate characters 6 through 9 to obtain seconds down to tenth of second ([6:10] is exclusive on upper bound)
        seconds = float(str(datetime.now().time())[6:10])
        if seconds < timer_start:
            seconds = seconds + 60
        return seconds - timer_start >= timer

    async def __timed_drive(self, speed, heading, direction, time_to_drive):
        # isolate characters 6 through 9 to obtain seconds down to tenth of second ([6:10] is exclusive on upper bound)
        timer_start = float(str(datetime.now().time())[6:10])
        while float(str(datetime.now().time())[6:10]) <= timer_start + time_to_drive:
            await self.__rvr.drive_with_heading(speed, heading, direction)
            await asyncio.sleep(0.1)
        await self.stop_raw_motors()
        return
