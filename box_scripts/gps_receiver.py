#!/usr/bin/env python3

import pynmea2
import traceback


class GpsReader:

    def __init__(self, serial_input):
        self._nmea_stream_reader = pynmea2.NMEAStreamReader()
        self._serial_input = serial_input

    def read_mainloop(self, callback = None):
        # (RMC, VTG)
        expected_data = GpsReader._empty_expected_data()
        while 1:
            gps_input = self._serial_input.readline()
            for gps_sentence in self._nmea_stream_reader.next(gps_input.decode("utf-8", errors="ignore")):
                try:
                    if isinstance(gps_sentence, pynmea2.types.talker.RMC):
                        expected_data["RMC"] = gps_sentence
                    elif isinstance(gps_sentence, pynmea2.types.talker.VTG):
                        expected_data["VTG"] = gps_sentence
                        # we assume that vtg is the last element that is read
                        if expected_data["RMC"] is not None and expected_data["VTG"] is not None:
                            if expected_data["RMC"].is_valid:
                                if callback is not None:
                                   callback(expected_data)
                                expected_data = GpsReader._empty_expected_data()
                                #self._serial_input.flush()
                            else:
                                print("invalid state")
                                print("expected_data[RMC]: {}".format(expected_data["RMC"]))
                                print("expected_data[VTG]: {}".format(expected_data["VTG"]))
                except Exception as e:
                    print("###### error ######")
                    print(e)
                    print("############")
                    self._serial_input.flush()
                    traceback.print_exc()

    @staticmethod
    def debug_gps_data(gps_data):
        print("RMC", gps_data["RMC"])
        print("VTG", gps_data["VTG"])

    @staticmethod
    def _empty_expected_data(self):
        return {"RMC": None,"VTG": None}


def main():
    with open('../samples/gps_samples.txt') as f:
        gps_reader = GpsReader(f)
        gps_reader.read_mainloop(GpsReader.debug_gps_data)


if __name__ == '__main__':
    main()
