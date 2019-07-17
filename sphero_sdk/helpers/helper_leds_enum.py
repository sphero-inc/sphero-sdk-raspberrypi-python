from enum import Enum

from sphero_sdk.common.enums.sphero_rvr_enums import SpheroRvrLedBitMasks as lbm


class RvrLeds(Enum):
    left_status_indication = lbm.left_status_indication_red |\
                             lbm.left_status_indication_green |\
                             lbm.left_status_indication_blue
    right_status_indication = lbm.right_status_indication_red |\
                              lbm.right_status_indication_green |\
                              lbm.right_status_indication_blue
    left_headlight = lbm.left_headlight_red |\
                     lbm.left_headlight_green |\
                     lbm.left_headlight_blue
    right_headlight = lbm.right_headlight_red |\
                      lbm.right_headlight_green |\
                      lbm.right_headlight_blue
    door_1 = lbm.door_1_red |\
             lbm.door_1_green |\
             lbm.door_1_blue
    door_2 = lbm.door_2_red |\
             lbm.door_2_green |\
             lbm.door_2_blue
    side_1 = lbm.side_1_red |\
             lbm.side_1_green |\
             lbm.side_1_blue
    side_2 = lbm.side_2_red |\
             lbm.side_2_green |\
             lbm.side_2_blue
    rear_1 = lbm.rear_1_red |\
             lbm.rear_1_green |\
             lbm.rear_1_blue
    rear_2 = lbm.rear_2_red |\
             lbm.rear_2_green |\
             lbm.rear_2_blue
    undercarriage_white = lbm.undercarriage_white