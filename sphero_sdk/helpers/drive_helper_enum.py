#!/usr/bin/env python

from enum import Enum


class RawMotorModes(Enum):
    '''IrCodes are the enums for the IrHelpers class
    '''
    stop = 0
    forward = 1
    reverse = 2

