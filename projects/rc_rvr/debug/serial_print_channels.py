import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from projects.rc_rvr.pysbus.sbus import SBUS
from projects.rc_rvr.pysbus.serial_parser import SerialParser
from projects.rc_rvr.pysbus.constants import SBUSConsts

tty = sys.argv[1]
baud = sys.argv[2]
sbus = SBUS(
    SerialParser(tty, baud)
)

channels = [0] * SBUSConsts.NUM_CHANNELS

sbus.begin()

try:
    while True:
        payload_ready, failsafe, lost_frame = sbus.read(channels)
        print(channels,"Payload: {0} | Failsafe: {1} | Lost Frame: {2}".format(payload_ready,failsafe,lost_frame))
finally:
    sbus.close()
    sys.exit(1)

