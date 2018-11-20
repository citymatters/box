from dht11 import DHT_11
from hpma115s import HPMA115S0
from gps_receiver import GpsReader
from cloud_syncer import CloudSyncer
import serial
import time
import json

GPS_UART = "/dev/ttyO1"
PM_UART = "/dev/ttyO4"


class SensorController:

    def __init__(self):
        gps_input = serial.Serial(GPS_UART, 9600)
        self._gps_parser = GpsReader(gps_input)
        self._gps_parser.read_mainloop(SensorController.gps_data_handler)

    @staticmethod
    def extract_gps(gps_data):
        lon_dir = gps_data["RMC"].lon_dir
        lon = float(gps_data["RMC"].lon)
        print("lon_dir", lon_dir)
        if lon_dir == "W":
            lon = lon * -1.0

        lat_dir = gps_data["RMC"].lat_dir
        lat = float(gps_data["RMC"].lat)
        if lat_dir == "S":
            lat = lat * -1.0
        return lat, lon

    @staticmethod
    def gps_data_handler(gps_data):
        # configuration
        disable_pm_sensor = True
        write_json_to_file = False

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
        pm_sensor.readBlockingSensorData()
        dht11_sensor_data = dht11.get_all_values()
        # convert to json
        lat_lon = SensorController.extract_gps(gps_data)

        json_data = {
            "sensor": "7ff15087-6bf0-4c74-aff5-260c7591caa2",
            "lat": lat_lon[0],
            "lon": lat_lon[1],
            "datetime": 1529150870,
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
