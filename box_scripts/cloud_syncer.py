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
        print("HTTP response:")
        print(response.read().decode('utf-8'))


def load_and_sync_recorded_data(filename):
    with open(filename, encoding='utf-8') as data_file:
        cloud_syncer = CloudSyncer()
        for line in data_file:
            json_line = json.loads(line)
            cloud_syncer.push_json(json_line)


def main():
    load_and_sync_recorded_data("debug_positions.txt")


if __name__ == '__main__':
    main()
