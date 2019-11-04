from .constants import SBUSConsts


class SBUS:
    def __init__(self, parser):
        self._parser = parser
        self._payload = [0]*SBUSConsts.PAYLOAD_SIZE

    def begin(self):
        self._parser.begin()

    def close(self):
        self._parser.close()

    def read(self, channels):

        failsafe = False
        lost_frame = False
        payload_ready = self._parser.parse(self._payload)

        if payload_ready:
            if channels is not None:
                payload = self._payload
                channels[0] = (payload[1] | payload[2] << 8) & 0x07FF
                channels[1] = (payload[2] >> 3 | payload[3] << 5) & 0x07FF
                channels[2] = (payload[3] >> 6 | payload[4] << 2 | payload[5] << 10) & 0x07FF
                channels[3] = (payload[5] >> 1 | payload[6] << 7) & 0x07FF
                channels[4] = (payload[6] >> 4 | payload[7] << 4) & 0x07FF
                channels[5] = (payload[7] >> 7 | payload[8] << 1 | payload[9] << 9) & 0x07FF
                channels[6] = (payload[9] >> 2 | payload[10] << 6) & 0x07FF
                channels[7] = (payload[10] >> 5 | payload[11] << 3) & 0x07FF
                channels[8] = (payload[12] | payload[13] << 8) & 0x07FF
                channels[9] = (payload[13] >> 3 | payload[14] << 5) & 0x07FF
                channels[10] = (payload[14] >> 6 | payload[15] << 2 | payload[16] << 10) & 0x07FF
                channels[11] = (payload[16] >> 1 | payload[17] << 7) & 0x07FF
                channels[12] = (payload[17] >> 4 | payload[18] << 4) & 0x07FF
                channels[13] = (payload[18] >> 7 | payload[19] << 1 | payload[20] << 9) & 0x07FF
                channels[14] = (payload[20] >> 2 | payload[21] << 6) & 0x07FF
                channels[15] = (payload[21] >> 5 | payload[22] << 3) & 0x07FF

                lost_frame = (payload[23] & SBUSConsts.SBUS_LOST_FRAME[0]) > 0
                failsafe = (payload[23] & SBUSConsts.SBUS_FAILSAFE[0]) > 0

        return payload_ready, failsafe, lost_frame

