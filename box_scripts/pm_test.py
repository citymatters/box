from hpma115s import HPMA115S0
import time

try:
    print("Starting")
    sensor = HPMA115S0("/dev/ttyO4")

    sensor.init()
    sensor.startParticleMeasurement()

    while 1:
        if (sensor.readParticleMeasurement()):
            print("PM2.5: %d ug/m3" % (sensor._pm2_5))
            print("PM10: %d ug/m3" % (sensor._pm10))

        time.sleep(1)

except KeyboardInterrupt:
    print("program stopped")
