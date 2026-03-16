import time
from pyb import Servo
import sensor
import math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positive
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

# The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
# x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
# translation the units are dimensionless and you must apply a conversion function.

# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
# divided by the y sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# c_x is the image x center position in pixels.
# c_y is the image y center position in pixels.

f_x = (2.8 / 3.6736) * 160  # find_apriltags defaults to this if not set
f_y = (2.8 / 2.7384) * 120  # find_apriltags defaults to this if not set
c_x = 160 * 0.5  # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5  # find_apriltags defaults to this if not set (the image.h * 0.5)
tagsizemm = 40


def degrees(radians):
    return (180 * radians) / math.pi

class dfr180(Servo):
    def __init__(self, pin, speed=1):
        super().__init__(pin)
        self.cur_angle = 90
        self.des_angle = 90
        self.speed = speed

    def set_angle(self, angle):
        self.pulse_width(int(angle * ((2400 - 600) / 180) + 600))

    def tick(self):
        self.cur_angle = (self.des_angle - self.cur_angle) * self.speed + self.cur_angle
        self.pulse_width(int(self.cur_angle * ((2400 - 600) / 180) + 600))


s1 = dfr180(1, 0.25)  # P7
s2 = dfr180(2, 0.25)  # P8


def tick_servos():
    s1.tick()
    s2.tick()


def translation_to_mm(translation, tag_size):
    # translation is in decimeters...
    return ((translation * 100) * tag_size) / 210


# def timer_sched(timer):
#     micropython.schedule(tickservos, 0)


# tim = Timer(4)
# tim.init(freq=100, callback=timer_sched)

time.sleep(1)

s1.set_angle(90)
s2.set_angle(90)

tx = None
while True:
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(
        fx=f_x, fy=f_y, cx=c_x, cy=c_y
    ):  # defaults to TAG36H11
        img.draw_rectangle(tag.rect, color=(255, 0, 0))
        img.draw_cross(tag.cx, tag.cy, color=(0, 255, 0))
        print_args = (
            tag.x_translation,
            tag.y_translation,
            tag.z_translation,
            degrees(tag.x_rotation),
            degrees(tag.y_rotation),
            degrees(tag.z_rotation),
        )
        # Translation units are unknown. Rotation units are in degrees.
        # print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
        tx = tag.x_translation
        ty = tag.y_translation
        tz = tag.z_translation
    if tx:
        # s1.set_angle(math.degrees(math.tan(tx / tz)) + 90)
        # s2.set_angle(math.degrees(math.tan(ty / tz)) + 90)
        # txadj = 5.30481 * tx + 1.58621
        # tyadj = -5.19884 * ty - 1.13968
        # tzadj = -28.51334 * tz + 3.92978
        txadj = translation_to_mm(tx, tagsizemm)
        tyadj = translation_to_mm(ty, tagsizemm)
        tzadj = translation_to_mm(tz, tagsizemm)
        s1.des_angle = 180 - (math.degrees(math.atan(tyadj / tzadj)) + 90)
        s2.des_angle = 180 - (math.degrees(math.atan(txadj / tzadj)) + 90)
        print(s1.des_angle, s2.des_angle)
        print(txadj, tzadj)
    # s1.tick()
    # s2.tick()
    tick_servos()
    # print(clock.fps())
