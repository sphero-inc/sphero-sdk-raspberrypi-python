#!/usr/bin/env python

import asyncio


# todo: once command queue is implemented, remove all asyncio.sleep(.5) calls after ir messages are sent
class InfraredControlAsync:
    """InfraredControlAsync is a class that serves as a helper for RVR's IR features by encapsulating complexities and
        removing the need for redundant function calls

    Args:
        rvr (AsyncSpheroRvr): Instance of an AsyncSpheroRvr with a reference to an event loop

    Returns:
    """

    def __init__(self, rvr):
        if rvr is None:
            raise TypeError("ERROR: A RVR OBJECT MUST BE PASSED IN AS A PARAMETER")

        self.__rvr = rvr

        return

    async def start_infrared_broadcasting(self, far_codes, near_codes):
        """Loops through lists of enums and broadcasts each IR code

        Args:
            far_codes (list): List of InfraredCodes for far code
            near_codes (list): List of InfraredCodes for near code

        Returns:
        """

        if far_codes is None:
            print('ERROR: FAR_CODES PARAMETER REQUIRES INPUT')

            return

        if near_codes is None:
            print('ERROR: NEAR_CODES PARAMETER REQUIRES INPUT')

            return

        if len(far_codes) == 0  or len(near_codes) == 0:
            print('ERROR: LISTS MUST BE OF LENGTH > 0')

            return

        if len(far_codes) != len(near_codes):
            print('ERROR: LISTS MUST BE THE SAME LENGTH')

            return

        zipped = zip(far_codes, near_codes)
        for code in zipped:
            await self.__rvr.start_robot_to_robot_infrared_broadcasting(code[0].value, code[1].value)
            await asyncio.sleep(.5)

        return

    async def stop_infrared_broadcasting(self):
        """Calls stop_robot_to_robot_infrared_broadcasting()

        Returns:
        """

        await self.__rvr.stop_robot_to_robot_infrared_broadcasting()

        return

    async def start_infrared_following(self, far_codes, near_codes):
        """Loops through lists of enums and broadcasts each IR code for following

        Args:
            far_codes (list): List of InfraredCodes for far code
            near_codes (list): List of InfraredCodes for near code

        Returns:
        """

        if far_codes is None:
            print('ERROR: FAR_CODES PARAMETER REQUIRES INPUT')

            return

        if near_codes is None:
            print('ERROR: NEAR_CODES PARAMETER REQUIRES INPUT')

            return

        if len(far_codes) == 0  or len(near_codes) == 0:
            print('ERROR: LISTS MUST BE OF LENGTH > 0')

            return

        if len(far_codes) != len(near_codes):
            print('ERROR: LISTS MUST BE THE SAME LENGTH')

            return

        zipped = zip(far_codes, near_codes)
        for code in zipped:
            await self.__rvr.start_robot_to_robot_infrared_following(code[0].value, code[1].value)
            await asyncio.sleep(.5)

        return

    async def stop_infrared_following(self):
        """Calls stop_robot_to_robot_infrared_following()

        Returns:
        """

        await self.__rvr.stop_robot_to_robot_infrared_following()

        return

    async def send_infrared_message(self, messages, strength=0):
        """Sends a single IR message for each element in the messages list

        Args:
            messages (list): List of InfraredCodes to send
            strength (uint8): Integer that represents emitter strength (0 - 64)

        Returns:
        """

        if messages is None:
            print('ERROR: MESSAGES PARAMETER REQUIRES INPUT')

            return

        if len(messages) == 0:
            print('ERROR: LIST MUST BE OF LENGTH > 0')

            return

        if strength < 0 or strength > 64:
            print('ERROR: STRENGTH MUST BE > 0 AND < 64')

            return

        for message in messages:
            await self.__rvr.send_robot_to_robot_infrared_message(
                message.value,
                strength,
                strength,
                strength,
                strength
            )

        return

    async def listen_for_infrared_message(self, handler, enable=True):
        """Listens for infrared messages on all channels

        Args:
            enable (bool): True to enable listening async; False to disable
            handler (func): Reference to message notification callback function -
                            requires one parameter called "infraredCode"
                            Ex. 'async def message_received_handler(infraredCode):'
        Returns:
        """

        if callable(handler):

            pass
        else:
            print('ERROR: HANDLER PARAMETER REQUIRES A FUNCTION REFERENCE AS INPUT')

            return

        if enable:
            asyncio.ensure_future(
                await self.__rvr.on_robot_to_robot_infrared_message_received_notify(
                    handler=handler
                )
            )
        else:
            pass    # TODO: remove existing future / handler?

        await self.__rvr.listen_for_robot_to_robot_infrared_message(enable)

        return

