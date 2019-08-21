import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import time
from sphero_sdk import SpheroRvrObserver

rvr = SpheroRvrObserver()


def handler1(major, minor, revision):
    print('{} {}.{}.{}'.format("Nordic", major, minor, revision))


def handler2(major, minor, revision):
    print('{} {}.{}.{}'.format("ST", major, minor, revision))


def main():
    rvr.get_main_application_version(handler1, target=1)

    time.sleep(0.5)

    rvr.get_main_application_version(handler2, target=2)

    time.sleep(0.5)

    rvr.close()


main()
