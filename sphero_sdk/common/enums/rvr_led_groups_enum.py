#!/usr/bin/env python

from enum import Enum

from sphero_sdk.common.enums.sphero_rvr_enums import SpheroRvrLedBitmasks

# TODO: autogen this file along with SpheroRvrLedBitmasks


class RvrLedGroups(Enum):
    status_indication_left = SpheroRvrLedBitmasks.left_status_indication_red | \
                             SpheroRvrLedBitmasks.left_status_indication_green | \
                             SpheroRvrLedBitmasks.left_status_indication_blue

    status_indication_right = SpheroRvrLedBitmasks.right_status_indication_red | \
                              SpheroRvrLedBitmasks.right_status_indication_green | \
                              SpheroRvrLedBitmasks.right_status_indication_blue

    headlight_left = SpheroRvrLedBitmasks.left_headlight_red | \
                     SpheroRvrLedBitmasks.left_headlight_green | \
                     SpheroRvrLedBitmasks.left_headlight_blue

    headlight_right = SpheroRvrLedBitmasks.right_headlight_red | \
                      SpheroRvrLedBitmasks.right_headlight_green | \
                      SpheroRvrLedBitmasks.right_headlight_blue

    battery_door_front = SpheroRvrLedBitmasks.battery_door_front_red | \
                         SpheroRvrLedBitmasks.battery_door_front_green | \
                         SpheroRvrLedBitmasks.battery_door_front_blue

    battery_door_rear = SpheroRvrLedBitmasks.battery_door_rear_red | \
                        SpheroRvrLedBitmasks.battery_door_rear_green | \
                        SpheroRvrLedBitmasks.battery_door_rear_blue

    power_button_front = SpheroRvrLedBitmasks.power_button_front_red | \
                         SpheroRvrLedBitmasks.power_button_front_green | \
                         SpheroRvrLedBitmasks.power_button_front_blue

    power_button_rear = SpheroRvrLedBitmasks.power_button_rear_red | \
                        SpheroRvrLedBitmasks.power_button_rear_green | \
                        SpheroRvrLedBitmasks.power_button_rear_blue

    brakelight_left = SpheroRvrLedBitmasks.left_brakelight_red | \
                      SpheroRvrLedBitmasks.left_brakelight_green | \
                      SpheroRvrLedBitmasks.left_brakelight_blue

    brakelight_right = SpheroRvrLedBitmasks.right_brakelight_red | \
                       SpheroRvrLedBitmasks.right_brakelight_green | \
                       SpheroRvrLedBitmasks.right_brakelight_blue

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

    undercarriage_white = SpheroRvrLedBitmasks.undercarriage_white
