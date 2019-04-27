import serial 




class SPS30:
    def __init__(self, port):
        self.__port = serial.Serial(port=port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE, timeout=2, xonxoff=False, rtscts=False,
                                    write_timeout=2, dsrdtr=False, inter_byte_timeout=None)
        self.__port.open()
        self.__start_stop_byte = bytes('0x7E')
        self.__error_codes = dict({0: 'No Error', 1: 'Wrong data length for this command (too much or little data)',
                                   2: 'Unknown command', 3: 'No access right for command',
                                   4: 'Illegal command parameter or parameter out of allowed range',
                                   40: 'Internal function argument out of range',
                                   67: 'Command not allowed in current state'})

        self.__sensor_commands = dict({0: 'Start Measurement', 1: 'Stop Measurement', 3: 'Read Measured Value',
                                       86: 'Start Fan Cleaning', 128: 'Read/Write Auto Cleaning Interval',
                                       208: 'Device Information', 211: 'Reset'})

    def __send_data(self, data):
        if isinstance(data, bytearray):
            try:
                self.__port.write(data)
            except serial.SerialTimeoutException:
                return -1
            except Exception as e:
                print(e)
                return -1
            return 0
        else:
            return -1

    def __read_data(self):
        read_data = bytearray()
        tmp_cnt = 0
        if self.__port.read(1) == b'\x7E':
            read_data += b'\x7E'
            tmp_data = b'\00'
            while tmp_data is not b'\x7E':
                tmp_data = self.__port.read(1)
                read_data += tmp_data
                tmp_cnt += 1
            # clear buffer
            self.__port.reset_input_buffer()
            return tmp_cnt, read_data
        else:
            self.__port.reset_input_buffer()
            return -1

    def __check_data_read(self, data):
        if isinstance(data, bytearray):
            data_str = data.decode()
            # remove bit stuffing
            data_str.replace('\x7D\x5E', '\x7E')
            data_str.replace('\x7D\x5D', '\x7D')
            data_str.replace('\x7D\x31', '\x11')
            data_str.replace('\x7D\x33', '\x13')
            ret_data = data_str.encode()
            return ret_data
        else:
            return -1

    def __calc_checksum(self,data):
        tmp_sum = 0
        if isinstance(data, bytearray):
            for element in data:
                tmp_sum += int.from_bytes(element, byteorder='little')
        else:
            return -1


    def __gen_output_frame(self, data):
