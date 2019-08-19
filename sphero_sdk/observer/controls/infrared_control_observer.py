#!/usr/bin/env python

import time


# todo: once command queue is implemented, remove all time.sleep(.5) calls after ir messages are sent
class InfraredControlObserver:
    """InfraredControlObserver is a class that serves as a helper for RVR's IR features by encapsulating complexities and
        removing the need for redundant function calls

    Args:
        rvr (ObserverSpheroRvr): Instance of an ObserverSpheroRvr

    Returns:
    """

    def __init__(self, rvr):
        if rvr is None:
            raise TypeError("ERROR: A RVR OBJECT MUST BE PASSED IN AS A PARAMETER")

        self.__rvr = rvr

        return

    def start_infrared_broadcasting(self, far_codes, near_codes):
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
            self.__rvr.start_robot_to_robot_infrared_broadcasting(code[0].value, code[1].value)
            time.sleep(.5)

        return

    def stop_infrared_broadcasting(self):
        """Calls stop_robot_to_robot_infrared_broadcasting()

        Returns:
        """

        self.__rvr.stop_robot_to_robot_infrared_broadcasting()

        return

    def start_infrared_following(self, far_codes, near_codes):
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
            self.__rvr.start_robot_to_robot_infrared_following(code[0].value, code[1].value)
            time.sleep(.5)

        return

    def stop_infrared_following(self):
        """Calls stop_robot_to_robot_infrared_following()

        Returns:
        """

        self.__rvr.stop_robot_to_robot_infrared_following()

        return

    def send_infrared_messages(self, messages, strength=0):
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
            self.__rvr.send_infrared_message(
                message.value,
                strength,
                strength,
                strength,
                strength
            )

        return

    def listen_for_infrared_message(self, handler, enable=True):
        """Listens for infrared messages on all channels and invokes given handler upon message received

        Args:
            enable (bool): True to enable listening async; False to disable

        Returns:
        """

        self.__rvr.enable_robot_infrared_message_notify(enable)

        self.__rvr.on_robot_to_robot_infrared_message_received_notify(handler)

        return
