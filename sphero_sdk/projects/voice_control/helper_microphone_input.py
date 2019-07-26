import sys
import pyaudio
import math
import struct
import wave
import time
import os
sys.path.append('/home/pi/raspberry-pi')
from sphero_sdk.projects.voice_control.helper_houndify import HoundifyHelper


Threshold = 10
short_normalize = (1.0/32768.0)
chunk = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
TIMEOUT_LENGTH = 1

f_name_directory = '/home/pi/.rvr_recordings'
f_name = '0.wav'


class Recorder:

    def __init__(self, instruction_queue):
        self.__p = pyaudio.PyAudio()
        self.__stream = self.__p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)
        self.__houndify_client = HoundifyHelper(instruction_queue)
        return

    def listen_forever(self):
        """listen_forever will constantly listen for audio, starting recordings when the volume exceeds a particular
        threshold and stopping them when the volume drops below that threshold. Recordings are saved as .wav files in
        the default location at the top of the script.

        Returns:

        """
        print('Listening')
        while True:
            audio = self.__stream.read(chunk, exception_on_overflow=False)
            rms_val = self.__rms(audio)
            if rms_val > Threshold:
                self.__record()
                print('Listening')

    def listen_once(self):
        """listen_once starts a recording when the volume exceeds a certain level and stops the recording when the
        volume dips below that threshold. Recordings are saved as .wav files in the default location at the top of the
        script.

        Returns:

        """
        keep_listening = True
        print('Listening')
        while keep_listening:
            audio = self.__stream.read(chunk, exception_on_overflow=False)
            rms_val = self.__rms(audio)
            if rms_val > Threshold:
                keep_listening = False
                self.__record()
        return

    def transcribe_file_houndify(self):
        """transcribe_file_houndify uses the Houndify service to transcribe an audio recording file.

        Returns:

        """
        self.listen_once()
        return self.__houndify_client.transcribe_file(f_name_directory + '/' + f_name)

    def transcribe_stream_houndify(self):
        """transcribe_stream_houndify uses the Houndify service to transcribe a stream of audio straight from a
        microphone

        Returns:

        """
        return self.__houndify_client.transcribe_stream(self.__stream)

    @staticmethod
    def __rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.__stream.read(chunk, exception_on_overflow=False)
            if self.__rms(data) >= Threshold:
                end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        self.__write(b''.join(rec))
        return

    def __write(self, recording):

        filename = os.path.join(f_name_directory, f_name)

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.__p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        return

