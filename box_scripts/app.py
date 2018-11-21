from dht11 import DHT_11
from hpma115s import HPMA115S0
from gps_receiver import GpsReader
from cloud_syncer import CloudSyncer
import serial
import time
import json
import pynmea2

GPS_UART = "/dev/ttyO1"
PM_UART = "/dev/ttyO4"


class SensorController:

    def __init__(self):
        gps_input = serial.Serial(GPS_UART, 9600)
        self._gps_parser = GpsReader(gps_input)
        self._gps_parser.read_mainloop(SensorController.gps_data_handler)

    @staticmethod
    def to_timestamp(gps_timestamp):
        print("gps timestamp : {} and type {}".format(gps_timestamp, type(gps_timestamp)))
        pynmea2_timestamp = pynmea2.timestamp(gps_timestamp)
        return time.mktime(pynmea2_timestamp.timetuple())

    @staticmethod
    def gps_data_handler(gps_data):
        # configuration
        disable_pm_sensor = False
        write_json_to_file = True

        # check if we don't move
        if float(gps_data["VTG"].spd_over_grnd_kmph) > 2.5:
            return

        # init sensor stuff
        pm_sensor = None

        if not disable_pm_sensor:
            pm_sensor = HPMA115S0(PM_UART)
            pm_sensor.init()
            pm_sensor.readParticleMeasurement()

        dht11 = DHT_11("P8_11")

        GpsReader.debug_gps_data(gps_data)

        # read sensor data
        if not disable_pm_sensor:
            pm_sensor.readBlockingSensorData()
        dht11_sensor_data = dht11.get_all_values()
        # convert to json

        json_data = {
            "sensor": "7ff15087-6bf0-4c74-aff5-260c7591caa2",
            "lat": gps_data["RMC"].latitude,
            "lon": gps_data["RMC"].longitude,
            "datetime": time.mktime(gps_data["RMC"].datetime.timetuple()),
            "data": [
                {
                    "type": "temperature",
                    "unit": "celsius",
                    "value": dht11_sensor_data[0]
                },
                {
                    "type": "humidity",
                    "unit": "rh",
                    "value": dht11_sensor_data[1]
                },
                {
                    "type": "pm2",
                    "unit": "ug/m3",
                    "value": 0 if disable_pm_sensor else int(pm_sensor._pm2_5)
                },
                {
                    "type": "pm10",
                    "unit": "ug/m3",
                    "value": 0 if disable_pm_sensor else int(pm_sensor._pm10)
                }
            ]
        }

        #close pm serial
        if not disable_pm_sensor:
            pm_sensor.closeSerial()

        # push to cloud
        if write_json_to_file:
            with open('debug_positions.txt', 'a') as debug_file:
                debug_file.write(json.dumps(json_data) + "\n")

        else:
            cloud_syncer = CloudSyncer()
            cloud_syncer.push_json(json_data)



        # for debugging
        print("sleep 10 seconds")
        time.sleep(10)


if __name__ == '__main__':
    SensorController()
