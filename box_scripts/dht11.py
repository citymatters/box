
import time as t
import Adafruit_DHT

PIN = 'P8_11'



class DHT_11:
    def __init__(self, pin):
        self._sensor_pin = pin
        self._sensor = Adafruit_DHT.DHT22
        self._current_temp = 0.0
        self._current_humi = 0.0

    def _update_values(self):
        self._current_humi, self._current_temp = Adafruit_DHT.read_retry(self._sensor, self._sensor_pin)


    def read_temperatur(self):
        self._update_values()
        return self._current_temp

    def read_thumidity(self):
        self._update_values()
        return self._current_humi

    def get_all_values(self):
        self._update_values()
        ret_list = list()
        ret_list.append(self._current_temp)
        ret_list.append(self._current_humi)
        #return list(self._current_temp, self._current_humi)
        return ret_list

def main():
    sensor = DHT_11(PIN)
    print("Read Sensor Values:")
    value_list = sensor.get_all_values()
    print("Current temperature : {} current humidity : {}".format(value_list[0], value_list[1]))


if __name__ == "__main__":
    main()
