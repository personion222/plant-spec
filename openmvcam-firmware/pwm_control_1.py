# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# PWM Control Example
#
# This example shows how to do PWM with your OpenMV Cam.

import time
from pyb import Pin, Timer

tim = Timer(4, freq=50)  # Frequency in Hz
ch1 = tim.channel(1, Timer.PWM, pin=Pin("P7"))
ch1.pulse_width_percent(7)

while True:
    time.sleep_ms(1000)
