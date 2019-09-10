import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def handler1(response):
    print('Response data for target 1 (Nordic):',response)


def handler2(response):
    print('Response data for target 2 (ST):',response)


def main():
    rvr.get_main_application_version(handler1, target=1)

    time.sleep(0.5)

    rvr.get_main_application_version(handler2, target=2)

    time.sleep(0.5)

    rvr.close()


main()
