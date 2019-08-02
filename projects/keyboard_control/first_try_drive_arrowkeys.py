import asyncio

from projects.keyboard_control import KeyboardHelper
from sphero_sdk.aio.client.dal.serial_async_dal import SerialAsyncDal
from sphero_sdk.aio.client.toys.async_sphero_rvr import AsyncSpheroRvr

# initialize global variables
key_helper = KeyboardHelper()
break_loop = False
red = [0xFF, 0x0, 0x0]
blue = [0x0, 0x0, 0xFF]
driving_keys = [119, 97, 115, 100, 113, 32]
speed = 64

loop = asyncio.get_event_loop()
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def set_all_leds(rgb_triples):
    await
    rvr.set_all_leds_with_32_bit_mask(
        0x3FFFFFFF,
        rgb_triples
    )
    await
    asyncio.sleep(.01)


def construct_blue():
    global red
    global blue
    colors = []
    for x in range(10):
        if (x % 2) == 0:
            colors.extend(red)
        else:
            colors.extend(blue)
    return colors


def construct_red():
    global red
    global blue
    colors = []
    for x in range(10):
        if (x % 2 - 1) == 0:
            colors.extend(red)
        else:
            colors.extend(blue)
    return colors


async def strobe_lights():
    lights_red = True
    while True:
        lights_red = not lights_red
        if lights_red:
            rgb_red = construct_red()
            await
            set_all_leds(rgb_red)
        else:
            rgb_blue = construct_blue()
            await
            set_all_leds(rgb_blue)
        await
        asyncio.sleep(0.25)


async def run_raw_motors(left_mode, left_speed, right_mode, right_speed):
    await
    rvr.raw_motors(left_mode, left_speed, right_mode, right_speed)


async def stop_raw_motors():
    await
    rvr.raw_motors(0, 0, 0, 0)


async def drive():
    global loop
    global break_loop
    global speed

    while key_helper.key_code not in driving_keys:
        await
        asyncio.sleep(0.05)

    print("Drive with key code: ", str(key_helper.key_code))

    if key_helper.key_code == 119:  # W
        await
        run_raw_motors(1, speed, 1, speed)
    elif key_helper.key_code == 97:  # A
        await
        run_raw_motors(2, speed, 1, speed)
    elif key_helper.key_code == 115:  # S
        await
        run_raw_motors(2, speed, 2, speed)
    elif key_helper.key_code == 100:  # D
        await
        run_raw_motors(1, speed, 2, speed)
    elif key_helper.key_code == 113:
        break_loop = True
    elif key_helper.key_code == 32:  # SPACE
        await
        stop_raw_motors()

    key_helper.key_code = -1


async def main():
    await
    rvr.wake()
    while True:
        await
        drive()


def run_loop():
    global loop
    loop.run_until_complete(
        asyncio.gather(
            main(),
            strobe_lights()
        )
    )


if __name__ == "__main__":
    loop.run_in_executor(None, key_helper.get_key_continuous)
    try:
        run_loop()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        key_helper.end_get_key_continuous()
        exit(1)
