#!/usr/bin/env python3


import pynmea2


class GpsReader:

    def __init__(self, filename):
        self._nmea_stream_reader = pynmea2.NMEAStreamReader(filename)

    def _empty_expected_data(self):
        return {"RMC" : None, "VTG" : None}

    def read_mainloop(self, callback = None):
        # (RMC, VTG)
        expected_data = self._empty_expected_data()

        while 1:
            for gps_sentence in self._nmea_stream_reader.next():
                try:
                    if isinstance(gps_sentence, pynmea2.types.talker.RMC):
                        expected_data["RMC"] = gps_sentence
                    elif isinstance(gps_sentence, pynmea2.types.talker.VTG):
                        expected_data["VTG"] = gps_sentence
                        # we assume that vtg is the last element that is read
                        if expected_data["RMC"] is not None and expected_data["VTG"] is not None:
                            if callback is not None:
                                callback(expected_data)
                            expected_data = self._empty_expected_data()

                except:
                    print("###### error ######")

    @staticmethod
    def debug_gps_data(gps_data):
        print("RMC", gps_data["RMC"])
        print("VTG", gps_data["VTG"])

def main():
    with open('../samples/gps_samples.txt') as f:
        gps_reader = GpsReader(f)
        gps_reader.read_mainloop(GpsReader.debug_gps_data)


if __name__ == '__main__':
    main()
