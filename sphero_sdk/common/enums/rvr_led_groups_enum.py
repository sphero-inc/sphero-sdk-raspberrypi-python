#!/usr/bin/env python

from enum import Enum

from sphero_sdk.common.enums.sphero_rvr_enums import SpheroRvrLedBitMasks

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
    battery_door_front = SpheroRvrLedBitMasks.battery_door_front_red | \
                         SpheroRvrLedBitMasks.battery_door_front_green | \
                         SpheroRvrLedBitMasks.battery_door_front_blue
    battery_door_rear = SpheroRvrLedBitMasks.battery_door_rear_red | \
                        SpheroRvrLedBitMasks.battery_door_rear_green | \
                        SpheroRvrLedBitMasks.battery_door_rear_blue
    power_button_front = SpheroRvrLedBitMasks.power_button_front_red | \
                         SpheroRvrLedBitMasks.power_button_front_green | \
                         SpheroRvrLedBitMasks.power_button_front_blue
    power_button_rear = SpheroRvrLedBitMasks.power_button_rear_red | \
                        SpheroRvrLedBitMasks.power_button_rear_green | \
                        SpheroRvrLedBitMasks.power_button_rear_blue
    brakelight_left = SpheroRvrLedBitMasks.left_brakelight_red | \
                      SpheroRvrLedBitMasks.left_brakelight_green | \
                      SpheroRvrLedBitMasks.left_brakelight_blue
    brakelight_right = SpheroRvrLedBitMasks.right_brakelight_red | \
                       SpheroRvrLedBitMasks.right_brakelight_green | \
                       SpheroRvrLedBitMasks.right_brakelight_blue
    all_lights = status_indication_left | \
                 status_indication_right | \
                 headlight_left | \
                 headlight_right | \
                 battery_door_front | \
                 battery_door_rear | \
                 power_button_front | \
                 power_button_rear | \
                 brakelight_left | \
                 brakelight_right
    undercarriage_white = SpheroRvrLedBitMasks.undercarriage_white
