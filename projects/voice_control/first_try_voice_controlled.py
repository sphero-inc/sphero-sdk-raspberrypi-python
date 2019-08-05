import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from text2digits import text2digits

from projects.voice_control.helper_microphone_input import Recorder
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from sphero_sdk.aio.controls.drive_control_async import DriveControlAsync
from sphero_sdk.aio.controls.led_control_async import LedControlAsync
from sphero_sdk.common.enums.colors_enums import Colors

loop = asyncio.get_event_loop()
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)
instruction_queue = []
DEFAULT_DISTANCE = 2
driver = DriveControlAsync(rvr)
recorder = Recorder(instruction_queue)
light_manager = LedControlAsync(rvr)
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
    await driver.reset_heading()
    await driver.drive_forward_seconds(0, 128, distance)
    print("DONE")


async def move_backward(instruction):
    global driver
    distance = search_for_int_in_string(instruction)
    print("MOVING BACKWARD " + str(distance))
    await driver.reset_heading()
    await driver.drive_backward_seconds(0, 128, distance)
    print("DONE")


async def turn_left(instruction):
    global driver
    distance = search_for_int_in_string(instruction)
    print("TURNING LEFT " + str(distance))
    await driver.reset_heading()
    await driver.turn_left_degrees(0, distance)
    print("DONE")


async def turn_right(instruction):
    global driver
    distance = search_for_int_in_string(instruction)
    print("TURNING RIGHT " + str(distance))
    await driver.reset_heading()
    await driver.turn_right_degrees(0, distance)
    print("DONE")


async def turn_on_lights(instruction):
    global light_manager
    words = instruction.split(" ")
    color = words[len(words) - 1].lower()
    print("TURNING LIGHTS", color)
    await light_manager.set_all_leds_color(Colors[color])
    print("DONE")


async def turn_off_lights():
    global light_manager
    print("TURNING LIGHTS OFF")
    await light_manager.turn_leds_off()
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
        elif "lights" in instruction and "set" in instruction:
            await turn_on_lights(instruction)
        elif "lights" in instruction and "off" in instruction:
            await turn_off_lights()


async def check_valid_instruction(instruction):
    if instruction == "":
        print("I'm sorry, I couldn't hear you. Please try again.\n")
        await light_manager.set_all_leds_color(Colors.red)
        await asyncio.sleep(.02)
    else:
        print("Processing instruction")
        instruction = t2d.convert(instruction)
        await light_manager.set_all_leds_color(Colors.green)
        await process_instructions(instruction)


async def listen_for_trigger(message):
    global recorder
    global light_manager
    if "rover" in message.lower():
        await light_manager.set_all_leds_color(Colors.yellow)
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
                # just say 'move' or 'set'
                # main_no_trigger()
                # say 'hey rvr'
                main_with_trigger()
            )
        )
    except KeyboardInterrupt:
        recorder.houndify.client.finish()
        print("\nExiting")
        exit(0)
