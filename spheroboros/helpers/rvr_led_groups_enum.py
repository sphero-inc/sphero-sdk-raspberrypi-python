#!/usr/bin/env python

from enum import Enum

from spheroboros.common.toys.sphero_rvr import SpheroRvrLedBitMasks

# TODO: autogen this file along with SpheroRvrLedBitMasks


class RvrLedGroups(Enum):
    status_indication_left = SpheroRvrLedBitMasks.left_status_indication_red | \
                             SpheroRvrLedBitMasks.left_status_indication_green | \
                             SpheroRvrLedBitMasks.left_status_indication_blue
    status_indication_right = SpheroRvrLedBitMasks.right_status_indication_red | \
                              SpheroRvrLedBitMasks.right_status_indication_green | \
                              SpheroRvrLedBitMasks.right_status_indication_blue
    headlight_left = SpheroRvrLedBitMasks.left_headlight_red | \
                     SpheroRvrLedBitMasks.left_headlight_green | \
                     SpheroRvrLedBitMasks.left_headlight_blue
    headlight_right = SpheroRvrLedBitMasks.right_headlight_red | \
                      SpheroRvrLedBitMasks.right_headlight_green | \
                      SpheroRvrLedBitMasks.right_headlight_blue
    battery_door_front = SpheroRvrLedBitMasks.door_1_red | \
                         SpheroRvrLedBitMasks.door_1_green | \
                         SpheroRvrLedBitMasks.door_1_blue
    battery_door_rear = SpheroRvrLedBitMasks.door_2_red | \
                        SpheroRvrLedBitMasks.door_2_green | \
                        SpheroRvrLedBitMasks.door_2_blue
    power_button_front = SpheroRvrLedBitMasks.side_1_red | \
                         SpheroRvrLedBitMasks.side_1_green | \
                         SpheroRvrLedBitMasks.side_1_blue
    power_button_rear = SpheroRvrLedBitMasks.side_2_red | \
                        SpheroRvrLedBitMasks.side_2_green | \
                        SpheroRvrLedBitMasks.side_2_blue
    brakelight_left = SpheroRvrLedBitMasks.rear_1_red | \
                      SpheroRvrLedBitMasks.rear_1_green | \
                      SpheroRvrLedBitMasks.rear_1_blue
    brakelight_right = SpheroRvrLedBitMasks.rear_2_red | \
                       SpheroRvrLedBitMasks.rear_2_green | \
                       SpheroRvrLedBitMasks.rear_2_blue
    undercarriage_white = SpheroRvrLedBitMasks.undercarriage_white
