# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Servo Control Example
#
# This example shows how to use your OpenMV Cam to control servos.

import time
# from pyb import Servo
from machine import LED

led = LED("LED_BLUE")

# s1 = Servo(1)  # P7
# s2 = Servo(2)  # P8
# s3 = Servo(3)  # P9

# s1.pulse_width(600)
# time.sleep(1)
# s1.pulse_width(2500)
# s2.pulse_width(1500)

time.sleep(3)
while True:
    led.on()
    # for i in range(100):
    #     s1.pulse_width(1000 + 10 * i)
    #     s2.pulse_width(1999 - 10 * i)
    #     # s3.pulse_width(1000 + i)
    #     time.sleep_ms(10)
    time.sleep(1)
    led.off()
    # for i in range(100):
    #     s1.pulse_width(1999 - 10 * i)
    #     s2.pulse_width(1000 + 10 * i)
    #     # s3.pulse_width(1999 - i)
    #     time.sleep_ms(10)
    time.sleep(1)
