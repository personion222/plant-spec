from machine import Pin
import time



def testfn(x):
    global lastpress
    if time.ticks_diff(time.ticks_ms(), lastpress) > 100:
        print("rise (debounce)")
        lastpress = time.ticks_ms()


lastpress = time.ticks_ms()
btnpin = Pin("P0", Pin.IN, Pin.PULL_UP)

btnpin.irq(testfn, Pin.IRQ_RISING)

while True:
    pass
