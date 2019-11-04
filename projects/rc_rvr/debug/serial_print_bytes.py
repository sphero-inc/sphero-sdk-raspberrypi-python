import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from projects.rc_rvr.pysbus.serial_parser import SerialParser

tty = sys.argv[1]
baud = int(sys.argv[2])
parser = SerialParser(tty, baud)
parser.begin()

try:
    while True:
        byte = parser.parse_raw()
        print(byte)
finally:
    parser.close()






