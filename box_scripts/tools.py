#!/usr/bin/python3

import os

class GPIO():

    def __init__(self, gpio_base_path, direction="in", value=0):
        if os.path.exists(gpio_base_path):
            self._base_path = gpio_base_path
            self._gpio_direction_path = self._base_path + str("/direction")
            self._gpio_value_path = self._base_path + str("/value")

            try:
                self.set_direction(direction)
                self.set_value(value)
            except:
                return -1

    def set_direction(self, direction):
        gpio_file = open(self._gpio_direction_path, "w")
        gpio_file.write(direction)
        gpio_file.close()

    def get_direction(self):
        gpio_file = open(self._gpio_direction_path, "r")
        direction = gpio_file.read()
        gpio_file.close()
        return direction

    def set_value(self, value):
        gpio_file = open(self._gpio_value_path, "w")
        gpio_file.write(str(value))
        gpio_file.close()

    def get_value(self):
        gpio_file = open(self._gpio_value_path, "r")
        value = gpio_file.read()
        gpio_file.close()
        return value
