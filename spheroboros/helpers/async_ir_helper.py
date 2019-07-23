#!/usr/bin/env python

import asyncio
from spheroboros.helpers.infrared_codes_enums import InfraredCodes


# todo: once command queue is implemented, remove all asyncio.sleep(.5) calls after ir messages are sent
class AsyncIrHelper:
    """InfraredControlAsync is a class that serves as a helper for RVR's IR features by encapsulating complexities and
        removing the need for redundant function calls

        :param rvr: (AsyncSpheroRvr): Instance of an AsyncSpheroRvr containing an event loop
        :return:
    """

    def __init__(self, rvr):
        if rvr is None:
            raise TypeError("ERROR: A RVR OBJECT MUST BE PASSED IN AS A PARAMETER")

        self.__rvr = rvr

        return

    async def start_infrared_broadcasting(self, far_codes, near_codes):
        """Begins infrared broadcasting on specified channels

        Args:
            far_codes (List<InfraredCodes>):
            near_codes (List<InfraredCodes>):

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

        :return:
        """

        await self.__rvr.stop_robot_to_robot_infrared_broadcasting()

        return

    async def start_infrared_following(self, far_codes, near_codes):
        """Loops through lists of enums and broadcasts each IR code for following

        :param far_codes: List of InfraredCodes for far code
        :param near_codes: List of InfraredCodes for near code
        :return:
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

        :return:
        """

        await self.__rvr.stop_robot_to_robot_infrared_following()

        return

    async def send_infrared_message(self, messages, strength=0):
        """Sends a single IR message for each element in the messages list

        :param messages: List of InfraredCodes to send
        :param strength: Integer that represents emitter strength (0 - 64)
        :return:
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
        """Listens for infrared messages on a list of channels

        :param channels: List of InfraredCodes to listen for
        :param handler: Reference to message notification callback function -
                        requires one parameter called "infraredCode"
        Ex. 'async def message_received_handler(infraredCode):'
        :param enable: Keyword argument to enable or disable listener
        :return:
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

        await self.__rvr.listen_for_robot_to_robot_infrared_message(0x00, enable)

        return

