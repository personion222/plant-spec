from pyb import Servo

class dfr180(Servo):
    def __init__(self, pin, speed=1, minlim=0, maxlim=180):
        super().__init__(pin)
        self.cur_angle = 90
        self.des_angle = 90
        self.speed = speed
        self.minlim = minlim
        self.maxlim = maxlim

    def set_angle(self, angle):
        self.cur_angle = max(min(angle, self.maxlim), self.minlim)
        self.pulse_width(int(max(min(angle, self.maxlim), self.minlim) * ((2400 - 600) / 180) + 600))

    def tick(self):
        self.cur_angle = (self.des_angle - self.cur_angle) * self.speed + self.cur_angle
        self.pulse_width(int(self.cur_angle * ((2400 - 600) / 180) + 600))
