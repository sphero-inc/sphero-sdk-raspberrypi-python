#!/usr/bin/env python

from datetime import datetime
import time

from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups
from sphero_sdk import LedControlObserver


class DriveControlObserver:
    """DriveControlObserver is a class that abstracts the driving process so that the user doesn't have to
        use the run_raw_motors command to drive RVR.

        Args:
            rvr (AsyncSpheroRvr): Instance of an AsyncSpheroRvr containing an event loop

        """

    __drive_no_flag = 0x00
    __drive_reverse_flag = 0x01

    def __init__(self, rvr):
        if rvr is None:
            raise TypeError('ERROR: PASS IN A RVR OBJECT')

        self.__rvr = rvr

        self.__led_control = LedControlObserver(self.__rvr)    # TODO: eventually call self.__rvr.led_control

        return

    def reset_heading(self):
        """reset_heading resets the heading of the RVR

        """
        print('reset heading...')
        self.__rvr.reset_yaw()

        return

    def drive_backward_seconds(self, speed=0, heading=0, time_to_drive=1):
        """drive_backward_seconds drives the RVR backward with a specified heading and speed for some number of seconds

        Args:
            speed (uint8): integer between 0 and 255
            heading (int): integer between 0 and 359
            time_to_drive (int): number of seconds to drive

        """
        print('drive backwards...')
        self.__timed_drive(speed, heading, DriveControlObserver.__drive_reverse_flag, time_to_drive)

        return

    def drive_forward_seconds(self, speed=0, heading=0, time_to_drive=1):
        """drive_forward_seconds drives the RVR forward with a specified heading and speed for some number of seconds

        Args:
            speed (uint8): integer between 0 and 255
            heading (int): integer between 0 and 359
            time_to_drive (int): number of seconds to drive

        """

        print('drive forward...')
        self.__timed_drive(speed, heading, DriveControlObserver.__drive_no_flag, time_to_drive)

        return

    def turn_left_degrees(self, heading, amount=90):
        """turn_left_degrees rotates the RVR counter-clockwise some number of degrees starting at a given heading. The
        rotation will default to 90 degrees if none is provided

        Args:
            heading (int): heading from where the turn will start
            amount (int): number of degrees to turn

        """
        self.__rvr.drive_with_heading(0, (heading - amount) % 360, DriveControlObserver.__drive_no_flag)
        time.sleep(0.5)

        return

    def turn_right_degrees(self, heading, amount=90):
        """turn_right_degrees rotates the RVR clockwise some number of degrees starting at a given heading. The
        rotation will default to 90 degrees if none is provided

        Args:
            heading (int): heading from where the turn will start (number between 0 and 359)
            amount (int): number of degrees to turn

        """
        self.__rvr.drive_with_heading(0, (heading + amount) % 360, DriveControlObserver.__drive_no_flag)
        time.sleep(0.5)

        return

    def roll_start(self, speed, heading):
        """roll_start rolls the RVR forward at a specified heading and speed

        Args:
            speed (int): driving speed -255 - 255(if negative, RVR drives backward)
            heading (int): direction to drive in

        """

        flags = 0

        if speed < 0:
            flags = flags | DriveControlObserver.__drive_reverse_flag

        speed = abs(speed)
        if speed > 255:
            speed = 255

        while heading < 0:
            heading += 360

        heading = heading % 360

        self.__rvr.drive_with_heading(speed, heading, flags)

        return

    def roll_stop(self, heading):
        """roll_stop stops the RVR and faces it towards a specified heading

        Args:
            heading (int): integer between 0 and 359

        """

        self.roll_start(0, heading) # REVERSE ARGS?

        return

    def set_heading(self, heading):
        """set_heading faces the RVR towards a specified heading

        Args:
            heading (int): integer between 0 and 359

        """

        self.roll_stop(heading)

        return

    def aim_start(self):
        """aim_start sets rear lights on RVR blue indicating the aiming process is starting

        """

        self.__led_control.set_multiple_leds_color(
            [RvrLedGroups.brakelight_left, RvrLedGroups.brakelight_right],
            [Colors.blue, Colors.blue]
        )

        return

    def aim_stop(self):
        """aim_stop turns the rear lights off and resets the heading of the RVR

        """
        # TODO: Add function for idling lights in the SDK
        self.reset_heading()

        self.__led_control.set_multiple_leds_color(
            [RvrLedGroups.brakelight_left, RvrLedGroups.brakelight_right],
            [Colors.off, Colors.off]
        )

        return

    def __timed_drive(self, speed, heading, flags, time_to_drive):
        timer_start = DriveControlObserver.__get_timer_seconds()

        while DriveControlObserver.__get_timer_seconds() <= timer_start + time_to_drive:
            self.__rvr.drive_with_heading(speed, heading, flags)
            time.sleep(0.1)

        self.__rvr.drive_with_heading(0, heading, flags)

        return

    @staticmethod
    def __get_timer_seconds():
        # isolate characters 6 through 9 to obtain seconds down to tenth of second ([6:10] is exclusive on upper bound)
        seconds = float(str(datetime.now().time())[6:10])

        return seconds
