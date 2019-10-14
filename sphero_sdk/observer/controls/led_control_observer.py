#!/usr/bin/env python
import time
from sphero_sdk import Colors
from sphero_sdk import RvrLedGroups


class LedControlObserver:
    """LedControlis a class that abstracts the process of manipulating RVR's lights so that the user doesn't have to
    use the raw sdk commands.

    Args:
        rvr (AsyncSpheroRvr): Instance of an AsyncSpheroRvr containing an event loop

    """

    def __init__(self, rvr):
        if rvr is None:
            raise TypeError('ERROR: PASS IN A RVR OBJECT')

        self.__rvr = rvr

        return

    def turn_leds_off(self):
        """turn_lights_off turns all the lights off on the rvr. It takes no inputs.

        """

        self.__rvr.set_all_leds(
            RvrLedGroups.all_lights.value,
            [color for i in range(10) for color in Colors.off.value]
        )

        time.sleep(1)

        return

    def set_led_rgb(self, led, red, green, blue):
        """set_led_rgb sets a single led on the RVR to a specified RGB value

        Args:
            led (RvrLeds): element from the enumeration RvrLeds
            red (uint8): integer between 0 and 255
            green (uint8): integer between 0 and 255
            blue (uint8): integer between 0 and 255

        """

        if not self.__is_color_valid(red, green, blue):
            raise ValueError('ERROR: RGB VALUES ARE INVALID')

        self.__rvr.set_all_leds(
            led.value,
            [red, green, blue]
        )

        return

    def set_led_color(self, led, color):
        """set_led_color sets a single light on the RVR to a specified color from the enumeration Color

        Args:
            led (RvrLeds): element from the enumeration RvrLeds
            color (Color): element from the enumeration Color

        """

        red, green, blue = color.value

        if not self.__is_color_valid(red, green, blue):
            raise ValueError('ERROR: RGB VALUES ARE INVALID')

        self.__rvr.set_all_leds(
            led.value,
            [red, green, blue]
        )

        return

    def set_all_leds_rgb(self, red, green, blue):
        """set_all_leds_rgb sets all of the lights on the RVR to a specified RGB value

        Args:
            red (uint8): integer between 0 and 255
            green (uint8): integer between 0 and 255
            blue (uint8): integer between 0 and 255

        """

        if not self.__is_color_valid(red, green, blue):
            raise ValueError('ERROR: RGB VALUES ARE INVALID')

        self.__rvr.set_all_leds(
            RvrLedGroups.all_lights.value,
            [color for x in range(0, 10) for color in [red, green, blue]]
        )

        return

    def set_all_leds_color(self, color):
        """set_all_leds_color sets all of the lights on the RVR to a specified color from the enumeration Color

        Args:
            color (Color): element from the enumeration Color

        """

        red, green, blue = color.value

        self.set_all_leds_rgb(red, green, blue)

        return

    def set_multiple_leds_with_enums(self, leds, colors):
        """set_multiple_leds_color sets multiple lights on the RVR to specified colors from the enumeration Color

        Args:
            lights [RvrLeds]: array of elements from RvrLeds enumeration
            colors [Color]: array of elements from Color enumeration

        """
        for i in range(len(leds)):
            self.set_led_color(
                leds[i], colors[i]
            )

        return

    def set_multiple_leds_with_rgb(self, leds, colors):
        """set_multiple_lights_enum sets multiple lights on the RVR to specified rgb values.
        The array of colors should be an array of integers whose size is a multiple of three.

        For example: set_multiple_lights_rgb([RvrLeds.door_1,RvrLeds.door_2],[255,0,0,255,0,0])
        will set both door lights to red

        Args:
            lights [RvrLeds]: array of elements from RvrLeds enumeration
            colors [int]: array of integers representing rgb triples

        """

        for i in range(len(leds)):
            self.set_led_rgb(
                leds[i],
                colors[i * 3],
                colors[i * 3 + 1],
                colors[i * 3 + 2]
            )

        return

    def __is_color_valid(self, red, green, blue):
        if self.__is_none(red) or self.__is_none(green) or self.__is_none(blue):
            return False
        if not self.__is_valid_rgb_values(red, green, blue):
            return False

        return True

    @staticmethod
    def __is_valid_rgb_values(red, green, blue):
        is_red_valid = 0 <= red <= 255
        is_green_valid = 0 <= green <= 255
        is_blue_valid = 0 <= blue <= 255

        return is_red_valid and is_green_valid and is_blue_valid

    @staticmethod
    def __is_none(value):
        return value is None
