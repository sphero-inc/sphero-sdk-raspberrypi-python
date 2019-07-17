#!/usr/bin/env python

import asyncio

from spheroboros import AsyncSpheroRvr
from spheroboros.helpers.helper_colors_enum import Color    # TODO: this file is missing


# TODO: ONCE COMMAND QUEUE IS IMPLEMENTED, REMOVE ALL ASYNCIO.SLEEP CALLS AFTER IR MESSAGES ARE SENT
# TODO: replace print statements with logging, unless specified otherwise
# TODO: instead of using r, g, b use red, green, blue (spell things out)
# TODO: validate red, green, blue parameter values are not None, and clamp the value to 0-255

class LedControlAsync:
    """LedControlAsync is a class that abstracts the process of manipulating RVR's lights so that the user doesn't have to
        use the raw sdk commands.

        Args:
            rvr (AsyncSpheroRvr): Instance of an AsyncSpheroRvr containing an event loop


        Returns:


        """

    def __init__(self, rvr):
        if rvr is None:
            print('ERROR: PASS IN A RVR OBJECT')    # TODO: raise StandardError

            return

        self.__rvr = rvr

        return

    async def turn_leds_off(self):
        """turn_lights_off turns all the lights off on the rvr. It takes no inputs.

        Args:

        Returns:


        """

        await self.__rvr.set_all_leds_with_64_bit_mask(
            0x3FFFFFFF, # TODO: this needs to reference the enum(s), and not be hardcoded
            [color for i in range(10) for color in Color.off.value]
        )

        await asyncio.sleep(1)

        return

    async def set_led_rgb(self, led, r, g, b):
        """set_led_rgb sets a single led on the RVR to a specified RGB value

        Args:
            led (RvrLeds): element from the enumeration RvrLeds
            r (int): integer between 0 and 255
            g (int): integer between 0 and 255
            b (int): integer between 0 and 255

        Returns:

        """

        await self.__rvr.set_all_leds_with_64_bit_mask(
            led.value,
            [r, g, b]
        )

        return

    async def set_led_color(self, led, color):
        """set_led_color sets a single light on the RVR to a specified color from the enumeration Color

        Args:
            led (RvrLeds): element from the enumeration RvrLeds
            color (Color): element from the enumeration Color

        Returns:

        """

        r, g, b = color.value

        await self.__rvr.set_all_leds_with_64_bit_mask(
            led.value,
            [r, g, b]
        )

        return

    async def set_all_leds_rgb(self, r, g, b):
        """set_all_leds_rgb sets all of the lights on the RVR to a specified RGB value

        Args:
            r (int): integer between 0 and 255
            g (int): integer between 0 and 255
            b (int): integer between 0 and 255

        Returns:

        """

        await self.__rvr.set_all_leds_with_64_bit_mask(
            0x3FFFFFFF, # TODO: this needs to reference the enum(s), and not be hardcoded
            [color for x in range(0, 10) for color in [r, g, b]]
        )

        return

    async def set_all_leds_color(self, color):
        """set_all_leds_color sets all of the lights on the RVR to a specified color from the enumeration Color

        Args:
            color (Color): element from the enumeration Color

        Returns:

        """

        r, g, b = color.value

        await self.set_all_leds_rgb(r, g, b)

        return

    async def set_multiple_leds_color(self, led, colors):
        """set_multiple_leds_color sets multiple lights on the RVR to specified colors from the enumeration Color

        Args:
            lights [RvrLeds]: array of elements from RvrLeds enumeration
            colors [Color]: array of elements from Color enumeration

        Returns:

        """

        for i in range(len(led)):
            await self.set_led_rgb(
                led[i],
                colors[i].value[0],
                colors[i].value[1],
                colors[i].value[2]
            )

        return

    async def set_multiple_leds_colors(self, leds, colors):
        """set_multiple_lights_enum sets multiple lights on the RVR to specified rgb values.
        The array of colors should be an array of integers whose size is a multiple of three.

        For example: set_multiple_lights_rgb([RvrLeds.door_1,RvrLeds.door_2],[255,0,0,255,0,0])
        will set both door lights to red

        Args:
            lights [RvrLeds]: array of elements from RvrLeds enumeration
            colors [int]: array of integers representing rgb triples

        Returns:

        """

        for i in range(len(leds)):
            await self.set_led_rgb(
                leds[i],
                colors[i * 3],
                colors[i * 3 + 1],
                colors[i * 3 + 2]
            )

        return
