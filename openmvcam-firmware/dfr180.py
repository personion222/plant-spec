from pyb import Servo

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
