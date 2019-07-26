#Libraries
import RPi.GPIO as GPIO
import asyncio

import sys
sys.path.append('/home/pi/raspberry-pi')
from spheroboros import AsyncSpheroRvr
from spheroboros import SerialAsyncDal
import time

loop = asyncio.get_event_loop()
rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)
GPIO.setmode(GPIO.BCM)
 

GPIO_TRIGGER = 18
GPIO_ECHO = 24
 

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


 
def distance():
    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time

    distance = (time_elapsed * 34300) / 2
    return distance
 

async def main():
    await rvr.wake()
    await rvr.reset_yaw()
    await asyncio.sleep(.5)
    while True:

        dist =  distance()
        await asyncio.sleep(.05)
        print("Measurement is {} cm".format(dist))
        if dist < 35:
            while dist < 35:
                await rvr.raw_motors(2,255,1,255)
                dist =  distance()
                await asyncio.sleep(.05)
                print('turning')
            await rvr.reset_yaw()
        if dist >= 35:
            await rvr.drive_with_heading(64, 0,0)
            await asyncio.sleep(.01)


try:
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()

