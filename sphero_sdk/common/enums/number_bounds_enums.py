from enum import IntEnum


class IntBounds(IntEnum):
    int_32_min = -2147483648
    int_32_max = 2147483647
    int_64_min = -9223372036854775808
    int_64_max = 9223372036854775807


class UintBounds(IntEnum):
    uint_8_max = 255
    uint_16_max = 65535
    uint_32_max = 4294967295
