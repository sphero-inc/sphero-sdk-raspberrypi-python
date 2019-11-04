import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from projects.rc_rvr.pysbus.serial_parser import SerialParser
from projects.rc_rvr.pysbus.constants import SBUSConsts

tty = sys.argv[1]
baud = sys.argv[2]
parser = SerialParser(tty, baud)
payload = [0] * SBUSConsts.PAYLOAD_SIZE

parser.begin()

try:
    while True:
        success = parser.parse(payload)
        length = SBUSConsts.PAYLOAD_SIZE
        hex_string = "["
        for i in range(length):
            hex_string += "{0:#0{1}x}".format(payload[i], 4)
            if i < length-1:
                hex_string += ", "
        hex_string += "] {0}".format(success)
        print(hex_string)
except:
    parser.close()
    sys.exit(1)
    raise()
