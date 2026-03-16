import time
from pyb import Servo
import csv

s1 = Servo(1)  # P7
s2 = Servo(2)  # P8
fov = 5

time.sleep(3)

with open("testfile.txt", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(("test1", "test2"))
    writer.writerow(("test3", "test4"))

for i in range(100):
    s1.pulse_width(500 + 20 * i)
    s2.pulse_width(2500 - 20 * i)
    time.sleep_ms(10)
time.sleep(1)
for i in range(100):
    s1.pulse_width(2500 - 20 * i)
    s2.pulse_width(500 + 20 * i)
    time.sleep_ms(10)
