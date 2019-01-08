#!/usr/bin/env python3

from sphero import SpheroRvr

rvr = SpheroRvr()

major, minor, build = rvr.get_main_app()

print('{}.{}.{}'.format(major, minor, build))
