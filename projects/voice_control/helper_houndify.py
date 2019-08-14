#!/usr/bin/env python3

import sys
sys.path.append('/home/pi/SDKs/houndify_python3_sdk_1.2.5/')
import time
import wave
import houndify
import pyaudio
try:
  import pySHSpeex
except ImportError:
  pass

transcription = None
CLIENT_ID = 's0fwMut-ItwNUdXVcyPIfQ=='
CLIENT_KEY = 'mqr_zxTQg4mApdj0vlKWkFSQa6XV3WXppGECvcP6ro9j1WuPLQuPgWXmiu9EirAPbrgn52oNS_3zSoa8U2MJ-Q=='
AUDIO_FILE = '/home/pi/.rvr_recordings/0.wav'
BUFFER_SIZE_FILE = 256
BUFFER_SIZE_STREAM = 512

request_info = {
    "RequestInfo": {
        "VoiceActivityDetection": {
            "MaxSilenceSeconds": 5,
            "MaxSilenceAfterFullQuerySeconds": 1
        },
        "RobotInfo": {
            "RobotConfiguration": {
                "LegCount": 2,
                "ArmCount": 2,
                "IsMobile": True,
                "Sensors": {
                    "HasCamera": False,
                    "HasVideoCamera": False
                }
            },
            "RobotState": {
                "CurrentAction": "Stationary",
                "RecordingVideo": False
            }
        }
    }
}

class HoundifyHelper:

    def __init__(self, instruction_queue):
        self.audio = None
        self.client_streaming = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "connor", enableVAD=True, requestInfo=request_info)
        self.client_file = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "test_user", enableVAD=False)

        self.listener = MyListener(instruction_queue)

    @staticmethod
    def check_for_errors(audio):
        if audio.getsampwidth() != 2:
            print("%s: wrong sample width (must be 16-bit)")
            sys.exit()
        if audio.getframerate() != 8000 and audio.getframerate() != 16000:
            print("%s: unsupported sampling frequency (must be either 8 or 16 khz)")
            sys.exit()
        if audio.getnchannels() != 1:
            print("%s: must be single channel (mono)")
            sys.exit()

    def transcribe_file(self, audio_file=AUDIO_FILE):
        self.audio = wave.open(audio_file)
        self.check_for_errors(self.audio)
        audio_size = self.audio.getnframes() * self.audio.getsampwidth()
        audio_duration = self.audio.getnframes() / self.audio.getframerate()
        chunk_duration = BUFFER_SIZE_FILE * audio_duration / audio_size
        self.client_file.setSampleRate(self.audio.getframerate())

        # # Uncomment the lines below to see an example of using a custom
        # # grammar for matching.  Use the file 'turnthelightson.wav' to try it.
        # clientMatches = [ {
        #   "Expression" : '([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].("turn"|"switch"|(1/100 "flip"))."on".["the"].("light"|"lights").[1/20 "for"."me"].[1/20 "please"])|([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].[100 ("turn"|"switch"|(1/100 "flip"))].["the"].("light"|"lights")."on".[1/20 "for"."me"].[1/20 "please"])|((("i".("want"|"like"))|((("i".["would"])|("i\'d")).("like"|"want"))).["the"].("light"|"lights").["turned"|"switched"|("to"."go")|(1/100"flipped")]."on".[1/20"please"])"',
        #   "Result" : { "Intent" : "TURN_LIGHT_ON" },
        #   "SpokenResponse" : "Ok, I\'m turning the lights on.",
        #   "SpokenResponseLong" : "Ok, I\'m turning the lights on.",
        #   "WrittenResponse" : "Ok, I\'m turning the lights on.",
        #   "WrittenResponseLong" : "Ok, I\'m turning the lights on."
        # } ]
        #
        # client.setHoundRequestInfo('ClientMatches', clientMatches)

        self.client_file.start(self.listener)

        while True:
            samples = self.audio.readframes(BUFFER_SIZE_FILE)
            if len(samples) == 0:
                break
            if self.client_file.fill(samples):
                break

        self.client_file.finish() 


    def transcribe_stream(self, stream):

        self.client_streaming.start(self.listener)

        ## Uncomment the lines below to see an example of using a custom
        ## grammar for matching.  Use the file 'turnthelightson.wav' to try it.
        # clientMatches = [ {
        #   "Expression" : '([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].("turn"|"switch"|(1/100 "flip"))."on".["the"].("light"|"lights").[1/20 "for"."me"].[1/20 "please"])|([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].[100 ("turn"|"switch"|(1/100 "flip"))].["the"].("light"|"lights")."on".[1/20 "for"."me"].[1/20 "please"])|((("i".("want"|"like"))|((("i".["would"])|("i\'d")).("like"|"want"))).["the"].("light"|"lights").["turned"|"switched"|("to"."go")|(1/100"flipped")]."on".[1/20"please"])"',
        #   "Result" : { "Intent" : "TURN_LIGHT_ON" },
        #   "SpokenResponse" : "Ok, I\'m turning the lights on.",
        #   "SpokenResponseLong" : "Ok, I\'m turning the lights on.",
        #   "WrittenResponse" : "Ok, I\'m turning the lights on.",
        #   "WrittenResponseLong" : "Ok, I\'m turning the lights on."
        # } ]
        # client.setHoundRequestInfo('ClientMatches', clientMatches)

        while True:
            samples = stream.read(BUFFER_SIZE_STREAM, exception_on_overflow=False)  
            if len(samples) == 0:
                break
            if self.client_streaming.fill(samples):
                break

        self.client_streaming.finish()

#
# Simplest HoundListener; just print out what we receive.
# You can use these callbacks to interact with your UI.
#
class MyListener(houndify.HoundListener):

    def __init__(self, instruction_queue):
        self.instruction_queue = instruction_queue

    def onPartialTranscript(self, transcript):
        print("Partial transcript: " + transcript)

    def onFinalResponse(self, response):
        print("\n\nRECEIVED FINAL RESPONSE")
        print(response)
        try:
            self.instruction_queue.append(response["AllResults"][0]["WrittenResponse"])
        except KeyError:
            pass

    def onError(self, err):
        print("Error: " + str(err))


if __name__ == "__main__":
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    output=True,
                    frames_per_buffer=512)
    queue = []
    test = HoundifyHelper(queue)
    test.transcribe_stream(stream)
    while len(queue) == 0:
        time.sleep(0.1)
    print(queue[0])
    test.client_streaming.finish()




