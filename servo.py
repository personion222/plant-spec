from time import sleep
import machine

pin = machine.Pin("P7", machine.Pin.OUT)

sleep(5)
print("pin on")
pin.on()
sleep(5)
print("pin off")
pin.off()
