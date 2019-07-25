import sys
import asyncio

sys.path.append('/home/pi/raspberry-pi')

from spheroboros.helpers.helper_drive import DriveHelper
from spheroboros.helpers.helper_microphone_input import Recorder
from spheroboros.helpers.helper_leds import HelperLEDs
from spheroboros.helpers.helper_colors_enum import Color
from spheroboros import AsyncSpheroRvr
from spheroboros import SerialAsyncDal
from text2digits import text2digits


loop = asyncio.get_event_loop()
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)
instruction_queue = []
DEFAULT_DISTANCE = 2
driver = DriveHelper(rvr)
recorder = Recorder(instruction_queue)
light_manager = HelperLEDs(rvr)
t2d = text2digits.Text2Digits()


def search_for_int_in_string(message):
    global DEFAULT_DISTANCE
    number = -1
    words = message.split(' ')
    for word in words:
        try:
            number = int(word)
        except ValueError:
            pass
    if number == -1:
        number = DEFAULT_DISTANCE
    return number


async def move_forward(instruction):
    global driver
    distance = search_for_int_in_string(instruction)
    print("MOVING FORWARD " + str(distance))
    await driver.drive_forward(128,distance)
    print("DONE")


async def move_backward(instruction):
    global driver
    distance = search_for_int_in_string(instruction)
    print("MOVING BACKWARD " + str(distance))
    await driver.drive_backward(128,distance)
    print("DONE")


async def turn_left(instruction):
    global driver
    distance = search_for_int_in_string(instruction)
    print("TURNING LEFT " + str(distance))
    await driver.turn_left(distance)
    print("DONE")


async def turn_right(instruction):
    global driver
    distance = search_for_int_in_string(instruction)
    print("TURNING RIGHT " + str(distance))
    await driver.turn_right(distance)
    print("DONE")


async def turn_on_lights(instruction):
    global light_manager
    words = instruction.split(" ")
    color = words[len(words)-1].upper()
    print("TURNING LIGHTS",color)
    await light_manager.set_all_lights_enum(Color[color])
    print("DONE")


async def turn_off_lights():
    global light_manager
    print("TURNING LIGHTS OFF")
    await light_manager.turn_lights_off()
    print("DONE")


async def process_instructions(message):
    instructions = message.split('and')
    for instruction in instructions:
        if "forward" in instruction:
            await move_forward(instruction)
        elif "back" in instruction:
            await move_backward(instruction)
        elif "left" in instruction:
            await turn_left(instruction)
        elif "right" in instruction:
            await turn_right(instruction)
        elif "lights" in instruction and "on" in instruction:
            await turn_on_lights(instruction)
        elif "lights" in instruction and "off" in instruction:
            await turn_off_lights()


async def check_valid_instruction(instruction):
    if instruction == "":
        print("I'm sorry, I couldn't hear you. Please try again.\n")
        await light_manager.set_all_lights_enum(Color.red)
        await asyncio.sleep(.02)
    else:
        print("Processing instruction")
        instruction = t2d.convert(instruction)
        await light_manager.set_all_lights_enum(Color.green)
        await process_instructions(instruction)


async def listen_for_trigger(message):
    global recorder
    global light_manager
    if "rover" in message.lower():
        await light_manager.set_all_lights_enum(Color.yellow)
        recorder.transcribe_stream_houndify()
        while len(instruction_queue) == 0:
            await asyncio.sleep(0.1)
        print("Received transcription")
        instruction = instruction_queue[0]
        instruction_queue.clear()
        await check_valid_instruction(instruction)


async def main_with_trigger():
    global rvr
    global recorder
    global light_manager
    await rvr.wake()
    while True:
        print("\nTranscribing the stream")
        recorder.transcribe_stream_houndify()
        while len(instruction_queue) == 0:
            await asyncio.sleep(0.1)
        print("Received transcription")
        instruction = instruction_queue[0]
        instruction_queue.clear()
        await listen_for_trigger(instruction)


async def main_no_trigger():
    global rvr
    global recorder
    global light_manager
    global instruction_queue
    await rvr.wake()
    while True:
        print("\nTranscribing the stream")
        recorder.transcribe_stream_houndify()
        while len(instruction_queue) == 0:
            await asyncio.sleep(0.1)
        print("Received transcription")
        instruction = instruction_queue[0]
        instruction_queue.clear()
        await check_valid_instruction(instruction)
        await asyncio.sleep(0.01)
        print("Going back to listening")


if __name__ == "__main__":
    try:
        loop.run_until_complete(
            asyncio.gather(
                main_no_trigger()
            )
        )
    except KeyboardInterrupt:
        recorder.houndify.client.finish()
        print("\nExiting")
        exit(0)
