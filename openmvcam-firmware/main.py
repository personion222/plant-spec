from machine import Pin, LED
import qwiic_as7265x
import vcnl4200
import dfr180
import sensor
import json
import time
import math
import os

r_led, g_led, b_led = LED("LED_RED"), LED("LED_GREEN"), LED("LED_BLUE")
r_led.on()
g_led.off()
b_led.off()


def toggle_running(_):
    global lastpress
    global running
    if time.ticks_diff(time.ticks_ms(), lastpress) > 1000:
        print("toggle running")
        lastpress = time.ticks_ms()
        running = not running

def get_all_measurements(board):
    board.take_measurements()
    return (
        board.get_a(),
        board.get_b(),
        board.get_c(),
        board.get_d(),
        board.get_e(),
        board.get_f(),
        board.get_g(),
        board.get_h(),
        board.get_r(),
        board.get_i(),
        board.get_s(),
        board.get_j(),
        board.get_t(),
        board.get_u(),
        board.get_v(),
        board.get_w(),
        board.get_k(),
        board.get_l()
    )

def translation_to_mm(translation, tag_size):
    # translation is in decimeters...
    return ((translation * 100) * tag_size) / 210


with open("config.json", 'r') as f:
    conf = json.load(f)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
sensor.set_brightness(2)

s1 = dfr180.dfr180(1, 0.25, minlim=40, maxlim=142)  # P7
s2 = dfr180.dfr180(2, 0.25, minlim=40, maxlim=142)  # P8
s1.set_angle(90)
s2.set_angle(90)

as7265x = qwiic_as7265x.QwiicAS7265x()
as7265x.disable_indicator()
as7265x.set_integration_cycles(conf["intcycles"])
as7265x.set_gain(0)

ir_amb_sens = vcnl4200.VCNL4200()

f_x = (2.8 / 3.6736) * 160
f_y = (2.8 / 2.7384) * 120
c_x = 160 * 0.5
c_y = 120 * 0.5

lastpress = time.ticks_ms()
btnpin = Pin("P0", Pin.IN, Pin.PULL_UP)
btnpin.irq(toggle_running, Pin.IRQ_RISING)
missionid = 0
homedir = os.listdir('/sdcard')
while f"mission-{missionid}" in homedir:
    missionid += 1
running = False
seen_tags = set()
out = {
    "entries": {},
    "missed": {},
    "tagsize": conf["tagsize"],
    "intcycles": conf["intcycles"],
    "fov": conf["fov"],
    "offset": conf["offset"]
}

while not running:
    pass

r_led.off()
g_led.on()
os.mkdir(f"mission-{missionid}")
os.mkdir(f"mission-{missionid}/pics")
startms = time.ticks_ms()
lastnotag = time.ticks_ms()

while running:
    img = sensor.snapshot()
    tags = img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y)
    if len(tags) == 0:
        lastnotag = time.ticks_ms()
        g_led.on()
        b_led.off()
    for tag in tags:
        g_led.off()
        b_led.on()
        img.draw_rectangle(tag.rect, color=(255, 0, 0))
        img.draw_cross(tag.cx, tag.cy, color=(0, 255, 0))
        tx = tag.x_translation
        ty = tag.y_translation
        tz = tag.z_translation
        txadj = translation_to_mm(tx, conf["tagsize"]) - 100 + conf["offset"][0]
        tyadj = translation_to_mm(ty, conf["tagsize"]) + 10 + conf["offset"][1]
        tzadj = -translation_to_mm(tz, conf["tagsize"]) - 50 + conf["offset"][2]
        if tag.id not in seen_tags and time.ticks_diff(time.ticks_ms(), lastnotag) > 300:
            seen_tags.add(tag.id)
            s1.set_angle(90)
            s2.set_angle(142)
            time.sleep_ms(200)
            cal1 = get_all_measurements(as7265x)
            print(txadj, tyadj, tzadj)
            s1.set_angle((math.degrees(math.atan(tyadj / tzadj)) + 90))
            s2.set_angle(180 - (math.degrees(math.atan(txadj / tzadj)) + 90))
            # s1.set_angle(90)
            # s2.set_angle(90)
            prox = ir_amb_sens.get_distance()
            amb = ir_amb_sens.get_ambient_light()
            time.sleep_ms(200)
            scan = get_all_measurements(as7265x)
            s1.set_angle(90)
            s2.set_angle(142)
            time.sleep_ms(200)
            cal2 = get_all_measurements(as7265x)
            calavg = tuple((w1 + w2) / 2 for w1, w2 in zip(cal1, cal2))
            img.save(f"mission-{missionid}/pics/{tag.id}.jpg")
            try:
                out["entries"][tag.id] = {
                    "ms": time.ticks_diff(time.ticks_ms(), startms),
                    "plant": conf["tags"][str(tag.id)]["plant"],
                    "water": conf["tags"][str(tag.id)]["water"],
                    "prox": prox,
                    "amb": amb,
                    "scanwl": scan,
                    "calwl": calavg
                }
            except KeyError:
                out["entries"][tag.id] = {
                    "ms": time.ticks_diff(time.ticks_ms(), startms),
                    "plant": None,
                    "water": None,
                    "prox": prox,
                    "amb": amb,
                    "scanwl": scan,
                    "calwl": calavg
                }

with open(f"mission-{missionid}/scans.json", 'w') as f:
    r_led.on()
    g_led.off()
    b_led.off()
    for key in conf["tags"].keys():
        if int(key) not in seen_tags:
            out["missed"][key] = {
                "ms": None,
                "plant": conf["tags"][key]["plant"],
                "water": conf["tags"][key]["water"],
                "prox": None,
                "amb": None,
                "scanwl": None,
                "calwl": None
            }
    json.dump(out, f)
    r_led.off()
