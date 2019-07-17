import asyncio

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import RgbColors


class LedsHelper:
    """HelperLEDs is a class that abstracts the process of manipulating RVR's lights so that the user doesn't have to
        use the raw sdk commands.

        Args:
            rvr (AsyncSpheroRvr): Instance of an AsyncSpheroRvr containing an event loop


        Returns:


        """

    def __init__(self, rvr):
        self.__rvr = rvr
        return

    async def turn_lights_off(self):
        """turn_lights_off turns all the lights off on the rvr. It takes no inputs.

        Args:

        Returns:


        """
        await self.__rvr.set_all_leds_with_32_bit_mask(
            0x3FFFFFFF,
            [color for i in range(10) for color in RgbColors.black.value]
        )
        await asyncio.sleep(1)
        return

    async def set_light_rgb(self, light, r, g, b):
        """set_light_rgb sets a single led on the RVR to a specified RGB value

        Args:
            light (RvrLeds): element from the enumeration RvrLeds
            r (int): integer between 0 and 255
            g (int): integer between 0 and 255
            b (int): integer between 0 and 255

        Returns:

        """
        await self.__rvr.set_all_leds_with_32_bit_mask(
            light.value,
            [r, g, b]
        )
        return

    async def set_light_enum(self, light, color):
        """set_light_enum sets a single light on the RVR to a specified color from the enumeration Color

        Args:
            light (RvrLeds): element from the enumeration RvrLeds
            color (RgbColors): element from the enumeration Color

        Returns:

        """
        r, g, b = color.value
        await self.__rvr.set_all_leds_with_32_bit_mask(
            light.value,
            [r, g, b]
        )
        return

    async def set_all_lights_rgb(self, r, g, b):
        """set_all_lights_rgb sets all of the lights on the RVR to a specified RGB value

        Args:
            r (int): integer between 0 and 255
            g (int): integer between 0 and 255
            b (int): integer between 0 and 255

        Returns:

        """
        await self.__rvr.set_all_leds_with_32_bit_mask(
            0x3FFFFFFF,
            [color for x in range(0,10) for color in [r, g, b]]
        )
        return

    async def set_all_lights_enum(self, color):
        """set_all_lights_enum sets all of the lights on the RVR to a specified color from the enumeration Color

        Args:
            color (RgbColors): element from the enumeration Color

        Returns:

        """
        r, g, b = color.value
        await self.set_all_lights_rgb(r, g, b)
        return

    async def set_multiple_lights_enum(self, lights, colors):
        """set_multiple_lights_enum sets multiple lights on the RVR to specified colors from the enumeration Color

        Args:
            lights [RvrLeds]: array of elements from RvrLeds enumeration
            colors [Color]: array of elements from Color enumeration

        Returns:

        """
        for i in range(len(lights)):
            await self.set_light_rgb(
                lights[i],
                colors[i].value[0],
                colors[i].value[1],
                colors[i].value[2]
            )
        return

    async def set_multiple_lights_rgb(self, lights, colors):
        """set_multiple_lights_enum sets multiple lights on the RVR to specified rgb values.
        The array of colors should be an array of integers whose size is a multiple of three.

        For example: set_multiple_lights_rgb([RvrLeds.door_1,RvrLeds.door_2],[255,0,0,255,0,0])
        will set both door lights to red

        Args:
            lights [RvrLeds]: array of elements from RvrLeds enumeration
            colors [int]: array of integers representing rgb triples

        Returns:

        """
        for i in range(len(lights)):
            await self.set_light_rgb(
                lights[i],
                colors[i*3],
                colors[i*3+1],
                colors[i*3+2]
            )
        return
