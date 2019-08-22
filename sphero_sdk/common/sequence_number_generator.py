#!/usr/bin/env python3


class SequenceNumberGenerator:
    """This class generates a 0-255 sequence number for outgoing API packets.
    """

    __sequence_number = 0

    @staticmethod
    def get_sequence_number():
        num = SequenceNumberGenerator.__sequence_number
        num += 1
        if num > 255:
            num = 0
        SequenceNumberGenerator.__sequence_number = num
        return num
