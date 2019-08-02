'''For use:
Pygame module attempts to open a game window accross the network from the Pi to a local machine. This 
requires X11 streaming. To use this script make sure that you have a client for X11 streaming installed
locally (I used XQuartz on Mac). Connect to the Pi using the -X flag: ssh -X pi@<ip-addr>
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import math
import asyncio
import pygame
from __future__ import absolute_import, division, unicode_literals, print_function

from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal

# initialize event loops and constants
pygame.init()
os.putenv('SDL_VIDEODRIVER', 'fbcon')
pygame.display.init()

screen_width = 800
screen_height = 800
center_x = screen_width / 2
center_y = screen_height / 2
win = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("RVR Controller")
mouse_position = [0, 0]
mouse_button_down = False
run_mouse_tracking = True

loop = asyncio.get_event_loop()
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)


async def run_raw_motors(left_mode, left_speed, right_mode, right_speed):
    global rvr
    await
    rvr.raw_motors(left_mode, left_speed, right_mode, right_speed)


async def stop_raw_motors():
    global rvr
    await
    rvr.raw_motors(0, 0, 0, 0)


def set_mouse_pos_on_click(event, x, y):
    global mouse_button_down
    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.mouse.set_pos([x, y])
        mouse_button_down = True


def set_mouse_pos_on_click_release(event, x, y):
    global mouse_button_down
    if event.type == pygame.MOUSEBUTTONUP:
        pygame.mouse.set_pos([x, y])
        mouse_button_down = False


def get_mouse_pos():
    global mouse_position
    mouse_position = pygame.mouse.get_pos()


def get_mouse_quadrant():
    x = mouse_position[0] - 400
    y = mouse_position[1] - 400

    if x > 0 and y <= 0:
        return 0
    elif x > 0 and y > 0:
        return 1
    elif x <= 0 and y > 0:
        return 2
    else:
        return 3


async def run_treads():
    global mouse_position
    global center_x
    global center_y
    global screen_height
    global mouse_button_down
    left_speed = 0
    right_speed = 0
    left_dir = 1
    right_dir = 1
    speed_constant = 180
    x = mouse_position[0] - 400
    y = mouse_position[1] - 400
    radius = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    scale = radius / 400
    mq = get_mouse_quadrant()
    angle = 0

    if x != 0:
        angle = math.fabs(math.degrees(math.atan(y / x)))

    if mq == 0:
        left_dir = 1
        left_speed = speed_constant * scale
        if math.fabs(y) > math.fabs(x):
            right_dir = 1
            right_speed = ((angle - 45) / 45) * speed_constant * scale
        else:
            right_dir = 2
            right_speed = ((45 - angle) / 45) * speed_constant * scale
    elif mq == 1:
        left_dir = 2
        left_speed = speed_constant * scale
        if math.fabs(y) > math.fabs(x):
            right_dir = 2
            right_speed = ((angle - 45) / 45) * speed_constant * scale
        else:
            right_dir = 1
            right_speed = ((45 - angle) / 45) * speed_constant * scale
    elif mq == 2:
        right_dir = 2
        right_speed = speed_constant * scale
        if math.fabs(y) > math.fabs(x):
            left_dir = 2
            left_speed = ((angle - 45) / 45) * speed_constant * scale
        else:
            left_dir = 1
            left_speed = ((45 - angle) / 45) * speed_constant * scale
    elif mq == 3:
        right_dir = 1
        right_speed = speed_constant * scale
        if math.fabs(y) > math.fabs(x):
            left_dir = 1
            left_speed = ((angle - 45) / 45) * speed_constant * scale
        else:
            left_dir = 2
            left_speed = ((45 - angle) / 45) * speed_constant * scale

    right_speed = int(math.fabs(round(right_speed)))
    left_speed = int(math.fabs(round(left_speed)))

    if mouse_button_down:
        await
        run_raw_motors(left_dir, left_speed, right_dir, right_speed)
        await
        asyncio.sleep(0.1)


def track_mouse():
    run = True
    while run:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            set_mouse_pos_on_click(event, screen_height / 2, screen_width / 2)
            set_mouse_pos_on_click_release(event, screen_height / 2, screen_width / 2)
        get_mouse_pos()


async def main():
    await
    rvr.wake()
    loop.run_in_executor(None, track_mouse)
    while True:
        await
        run_treads()


try:
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(1)
