import qwiic_as7265x
import machine
import sys

print(qwiic_as7265x.__file__)

def runExample():
    leds = (machine.LED("LED_RED"), machine.LED("LED_GREEN"), machine.LED("LED_BLUE"))
    onled = 0
    leds[onled].on()
    print("\nQwiic Spectral Triad Example 1 - Basic\n")

    myAS7265x = qwiic_as7265x.QwiicAS7265x()

    if myAS7265x.is_connected() == False:
        print("The device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    if myAS7265x.begin() == False:
        print("Unable to initialize the AS7265x. Please check your connection", file = sys.stderr)
        return

    print("A,B,C,D,E,F,G,H,R,I,S,J,T,U,V,W,K,L")

    myAS7265x.disable_indicator()

    while True:
        myAS7265x.take_measurements()
        sum410535 = sum((
            myAS7265x.get_calibrated_a(),
            myAS7265x.get_calibrated_b(),
            myAS7265x.get_calibrated_c(),
            myAS7265x.get_calibrated_d(),
            myAS7265x.get_calibrated_e(),
            myAS7265x.get_calibrated_f()))

        sum560705 = sum((
            myAS7265x.get_calibrated_g(),
            myAS7265x.get_calibrated_h(),
            myAS7265x.get_calibrated_r(),
            myAS7265x.get_calibrated_i(),
            myAS7265x.get_calibrated_s(),
            myAS7265x.get_calibrated_j()))

        sum730940 = sum((
            myAS7265x.get_calibrated_t(),
            myAS7265x.get_calibrated_u(),
            myAS7265x.get_calibrated_v(),
            myAS7265x.get_calibrated_w(),
            myAS7265x.get_calibrated_k(),
            myAS7265x.get_calibrated_l()))

        print(str(myAS7265x.get_calibrated_a()) + ",", end="")  # 410nm
        print(str(myAS7265x.get_calibrated_b()) + ",", end="")  # 435nm
        print(str(myAS7265x.get_calibrated_c()) + ",", end="")  # 460nm
        print(str(myAS7265x.get_calibrated_d()) + ",", end="")  # 485nm
        print(str(myAS7265x.get_calibrated_e()) + ",", end="")  # 510nm
        print(str(myAS7265x.get_calibrated_f()) + ",", end="")  # 535nm

        print(str(myAS7265x.get_calibrated_g()) + ",", end="")  # 560nm
        print(str(myAS7265x.get_calibrated_h()) + ",", end="")  # 585nm
        print(str(myAS7265x.get_calibrated_r()) + ",", end="")  # 610nm
        print(str(myAS7265x.get_calibrated_i()) + ",", end="")  # 645nm
        print(str(myAS7265x.get_calibrated_s()) + ",", end="")  # 680nm
        print(str(myAS7265x.get_calibrated_j()) + ",", end="")  # 705nm

        print(str(myAS7265x.get_calibrated_t()) + ",", end="")  # 730nm
        print(str(myAS7265x.get_calibrated_u()) + ",", end="")  # 760nm
        print(str(myAS7265x.get_calibrated_v()) + ",", end="")  # 810nm
        print(str(myAS7265x.get_calibrated_w()) + ",", end="")  # 860nm
        print(str(myAS7265x.get_calibrated_k()) + ",", end="")  # 900nm
        print(str(myAS7265x.get_calibrated_l()))  # 940nm
        # print(sum410535, sum560705, sum730940)

        if max(sum410535, sum560705, sum730940) == sum410535:
            if onled != 0:
                leds[onled].off()
                onled = 0
                leds[onled].on()

        if max(sum410535, sum560705, sum730940) == sum560705:
            if onled != 1:
                leds[onled].off()
                onled = 1
                leds[onled].on()

        if max(sum410535, sum560705, sum730940) == sum730940:
            if onled != 2:
                leds[onled].off()
                onled = 2
                leds[onled].on()

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print(exErr)
        print("\nEnding Example")
        sys.exit(0)
