import time
from dfr180 import dfr180
import qwiic_as7265x
import csv
import os


def get_all_measurements(as7265x):
    as7265x.take_measurements()
    return {
        'A': as7265x.get_calibrated_a(),
        'B': as7265x.get_calibrated_b(),
        'C': as7265x.get_calibrated_c(),
        'D': as7265x.get_calibrated_d(),
        'E': as7265x.get_calibrated_e(),
        'F': as7265x.get_calibrated_f(),
        'G': as7265x.get_calibrated_g(),
        'H': as7265x.get_calibrated_h(),
        'R': as7265x.get_calibrated_r(),
        'I': as7265x.get_calibrated_i(),
        'S': as7265x.get_calibrated_s(),
        'J': as7265x.get_calibrated_j(),
        'T': as7265x.get_calibrated_t(),
        'U': as7265x.get_calibrated_u(),
        'V': as7265x.get_calibrated_v(),
        'W': as7265x.get_calibrated_w(),
        'K': as7265x.get_calibrated_k(),
        'L': as7265x.get_calibrated_l()
    }


s1min, s1max = 70, 110
s2min, s2max = 70, 110
s1 = dfr180(1, minlim=s1min, maxlim=s1max)
s2 = dfr180(2, minlim=s2min, maxlim=s2max)
as7265x = qwiic_as7265x.QwiicAS7265x()
as7265x.disable_indicator()
as7265x.set_integration_cycles(255)
as7265x.set_gain(3)
fov = 10
wavelens = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'R', 'I', 'S', 'J', 'T', 'U', 'V', 'W', 'K', 'L')

time.sleep(3)

nametime = time.time()
os.mkdir(f"spect_imgs/{nametime}")
files = {wl: open(f"spect_imgs/{nametime}/{nametime}{wl}.csv", 'w') for wl in wavelens}
writers = {wl: csv.writer(f) for wl, f in files.items()}

for i in range(s1min, s1max, fov * 2):
    row1 = {wl: [] for wl in wavelens}
    row2 = {wl: [] for wl in wavelens}
    s1.set_angle(i)

    for j in range(s2min, s2max + fov, fov):
        s2.set_angle(j)
        # time.sleep_ms(10)
        measurements = get_all_measurements(as7265x)
        for wl in wavelens:
            row1[wl].append(str(measurements[wl]))

    s1.set_angle(i + fov)

    for j in range(s2max, s2min - fov, -fov):
        s2.set_angle(j)
        # time.sleep_ms(10)
        measurements = get_all_measurements(as7265x)
        for wl in wavelens:
            row2[wl].append(str(measurements[wl]))

    for wl, writer in writers.items():
        writer.writerow(row1[wl])
        writer.writerow(row2[wl][::-1])

for f in files.values():
    f.close()
