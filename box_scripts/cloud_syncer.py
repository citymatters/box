#!/usr/bin/env python3

import urllib.request, urllib.parse
import json


class CloudSyncer:

    CITY_MATTERS_POST_URL = "https://smartcountryhacks.citymatters.de/api/add"

    def __init__(self, post_url = CITY_MATTERS_POST_URL):
        self._post_url = post_url

    def push_json(self, json_data):
        json_params = json.dumps(json_data).encode('utf8')
        req = urllib.request.Request(self._post_url, data=json_params,
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        print("HTTP response:");
        print(response.read().decode('utf-8'));




def push_test_data():
    test_datagram = {"sensor": "7ff15087-6bf0-4c74-aff5-260c7591caa2", "lat": 48.377553, "lon": 11.755498,
                     "alt": 800.000, "datetime": 1529150870,
                     "data": [{"type": "temperature", "unit": "celsius", "value": 222.3},
                              {"type": "humidity", "unit": "rh", "value": 88.0},
                              {"type": "pm2", "unit": "µg/m3", "value": 77},
                              {"type": "pm10", "unit": "µg/m3", "value": 77}]}
    cloud_syncer = CloudSyncer()
    cloud_syncer.push_json(test_datagram)


def main():
    push_test_data()


if __name__ == '__main__':
    main()
