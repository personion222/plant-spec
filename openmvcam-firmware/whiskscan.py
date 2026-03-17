import time
from dfr180 import dfr180
import qwiic_as7265x
import csv

s1min, s1max = 60, 120
s2min, s2max = 60, 120
s1 = dfr180(1, minlim=s1min, maxlim=s1max)
s2 = dfr180(2, minlim=s2min, maxlim=s2max)
as7265x = qwiic_as7265x.QwiicAS7265x()
as7265x.disable_indicator()
as7265x.set_integration_cycles(128)
fov = 5
wavelens = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'R', 'I', 'S', 'J', 'T', 'U', 'V', 'W', 'K', 'L')

time.sleep(3)

nametime = time.time()
files = {wl: open(f"spect_imgs/{nametime}{wl}.csv", 'w') for wl in wavelens}
writers = {wl: csv.writer(f) for wl, f in files.items()}

for i in range(s1min, s1max, fov * 2):
    row1 = {wl: [] for wl in wavelens}
    row2 = {wl: [] for wl in wavelens}
    s1.set_angle(i)

    for j in range(s2min, s2max, fov):
        s2.set_angle(j)
        # time.sleep_ms(10)
        as7265x.take_measurements()
        row1['A'].append(str(as7265x.get_calibrated_a()))
        row1['C'].append(str(as7265x.get_calibrated_c()))
        row1['D'].append(str(as7265x.get_calibrated_d()))
        row1['E'].append(str(as7265x.get_calibrated_e()))
        row1['F'].append(str(as7265x.get_calibrated_f()))
        row1['G'].append(str(as7265x.get_calibrated_g()))
        row1['H'].append(str(as7265x.get_calibrated_h()))
        row1['R'].append(str(as7265x.get_calibrated_r()))
        row1['I'].append(str(as7265x.get_calibrated_i()))
        row1['S'].append(str(as7265x.get_calibrated_s()))
        row1['J'].append(str(as7265x.get_calibrated_j()))
        row1['T'].append(str(as7265x.get_calibrated_t()))
        row1['U'].append(str(as7265x.get_calibrated_u()))
        row1['V'].append(str(as7265x.get_calibrated_v()))
        row1['W'].append(str(as7265x.get_calibrated_w()))
        row1['K'].append(str(as7265x.get_calibrated_k()))
        row1['L'].append(str(as7265x.get_calibrated_l()))
        row1['B'].append(str(as7265x.get_calibrated_b()))

    s1.set_angle(i + fov)

    for j in range(s2max, s2min, -fov):
        s2.set_angle(j)
        # time.sleep_ms(10)
        as7265x.take_measurements()
        row2['A'].append(str(as7265x.get_calibrated_a()))
        row2['C'].append(str(as7265x.get_calibrated_c()))
        row2['D'].append(str(as7265x.get_calibrated_d()))
        row2['E'].append(str(as7265x.get_calibrated_e()))
        row2['F'].append(str(as7265x.get_calibrated_f()))
        row2['G'].append(str(as7265x.get_calibrated_g()))
        row2['H'].append(str(as7265x.get_calibrated_h()))
        row2['R'].append(str(as7265x.get_calibrated_r()))
        row2['I'].append(str(as7265x.get_calibrated_i()))
        row2['S'].append(str(as7265x.get_calibrated_s()))
        row2['J'].append(str(as7265x.get_calibrated_j()))
        row2['T'].append(str(as7265x.get_calibrated_t()))
        row2['U'].append(str(as7265x.get_calibrated_u()))
        row2['V'].append(str(as7265x.get_calibrated_v()))
        row2['W'].append(str(as7265x.get_calibrated_w()))
        row2['K'].append(str(as7265x.get_calibrated_k()))
        row2['L'].append(str(as7265x.get_calibrated_l()))
        row2['B'].append(str(as7265x.get_calibrated_b()))

    for wl, writer in writers.items():
        writer.writerow(row1[wl])
        writer.writerow(row2[wl])

for f in files.values():
    f.close()
