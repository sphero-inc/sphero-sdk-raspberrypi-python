#!/usr/bin/env python

import time


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
            raise TypeError('far_codes parameter requires input')

        if near_codes is None:
            raise TypeError('near_codes parameter requires input')

        if len(far_codes) == 0 or len(near_codes) == 0:
            raise ValueError('lists near_codes and far_codes must have at least one element')

        if len(far_codes) != len(near_codes):
            raise ValueError('lists near_codes and far_codes must have the same number of elements')

        for far_code, near_code in zip(far_codes, near_codes):
            self.__rvr.start_robot_to_robot_infrared_broadcasting(far_code.value, near_code.value)
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
            raise TypeError('far_codes parameter requires input')

        if near_codes is None:
            raise TypeError('near_codes parameter requires input')

        if len(far_codes) == 0 or len(near_codes) == 0:
            raise ValueError('lists near_codes and far_codes must have at least one element')

        if len(far_codes) != len(near_codes):
            raise ValueError('lists near_codes and far_codes must have the same number of elements')

        for far_code, near_code in zip(far_codes, near_codes):
            self.__rvr.start_robot_to_robot_infrared_following(far_code.value, near_code.value)
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
            raise TypeError('messages parameter requires input')

        if len(messages) == 0:
            raise ValueError('list messages must have at least one element')

        if strength < 0 or strength > 64:
            raise ValueError('parameter strength must be greater than or equal to 0 and less than or equal 64')

        for message in messages:
            self.__rvr.send_infrared_message(
                message.value,
                strength,
                strength,
                strength,
                strength
            )

        return

    def listen_for_infrared_message(self, handler):
        """Listens for infrared messages on all channels and invokes given handler upon message received

        Args:
            enable (bool): True to enable listening async; False to disable

        Returns:
        """

        self.__rvr.enable_robot_infrared_message_notify(enable)

        self.__rvr.on_robot_to_robot_infrared_message_received_notify(handler)

        return
