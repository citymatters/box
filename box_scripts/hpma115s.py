import time
import serial

READ_PARTICLE_MEASUREMENT = 4
HPM_READ_PARTICLE_MEASUREMENT_LEN = 5
HPM_MAX_RESP_SIZE = 8
HPM_CMD_RESP_HEAD = 0x40


class HPMA115S0:
    _serial = None
    _pm2_5 = None
    _pm10 = None
    _dataBuf = [None] * (HPM_READ_PARTICLE_MEASUREMENT_LEN - 1)

    def __init__(self, ser):
        """
        Constructor for the HPMA115S0 class
        """
        self._serial = serial.Serial()
        self._serial.port = ser
        self._serial.baudrate = 9600
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = 1
        self._serial.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeSerial()

    def closeSerial(self):
        self._serial.close()

    def init(self):
        """
        Function which initializes the sensor.
        """
        print("Initializing")
        time.sleep(0.1)
        self.startParticleMeasurement()
        time.sleep(0.1)
        self.disableAutoSend()

    def sendCmd(self, cmdBuf):
        """
        Function which sends a serial command to the sensor (cf datasheet)

        Params:
                cmdBuf: the array containing the datas to be sent
        """
        self._serial.write(bytearray(cmdBuf))

    def readCmdResp(self, cmdType):
        """
        Function which reads command response from the sensor

        Params: 
                cmdType : Expected command type
        """
        respBuf = [None] * HPM_MAX_RESP_SIZE
        respIdx = 0
        calChecksum = 0
        for i in range(0, len(respBuf)):
            respBuf[i] = 0

        if (self.readStringUntil(HPM_CMD_RESP_HEAD)):
            respBuf[0] = HPM_CMD_RESP_HEAD
            respBuf[1] = ord(self._serial.read())

            if (respBuf[1] and ((respBuf[1] + 1) <= len(respBuf) - 2) and (respBuf[1] - 1) <= len(self._dataBuf)):
                resp = self.readBytes(respBuf, respBuf[1] + 1, 2)
                respBuf = resp[0]
                respCount = resp[1]
                if (respCount == respBuf[1] + 1):
                    if (respBuf[2] == cmdType):
                        while (respIdx < (2 + respBuf[1])):
                            calChecksum += respBuf[respIdx]
                            respIdx += 1
                        calChecksum = (65536 - calChecksum) % 256
                        if (calChecksum == respBuf[2 + respBuf[1]]):
                            print("received valid data")
                            for i in range(0, len(self._dataBuf)):
                                self._dataBuf[i] = 0
                            j = 0
                            for i in range(0, 4):
                                self._dataBuf[j] = respBuf[i + 3]
                                j += 1
                            return (respBuf[1] - 1)
        return False

    def startParticleMeasurement(self):
        """
        Function which starts sensor measurement
        """
        cmd = [0x68, 0x01, 0x01, 0x96]
        self.sendCmd(cmd)

    def stopParticleMeasurement(self):
        """
        Function which stops sensor measurement
        """
        cmd = [0x68, 0x01, 0x02, 0x95]
        self.sendCmd(cmd)

    def disableAutoSend(self):
        """
        Function which stops auto send by the sensor
        """
        cmd = [0x68, 0x01, 0x20, 0x77]
        self.sendCmd(cmd)

    def readParticleMeasurement(self):
        """
        Function which sends a read command to sensor to get retrieve datas
        """
        cmdBuf = [0x68, 0x01, 0x04, 0x93]

        self.sendCmd(cmdBuf)

        if (self.readCmdResp(READ_PARTICLE_MEASUREMENT) == (HPM_READ_PARTICLE_MEASUREMENT_LEN - 1)):
            self._pm2_5 = self._dataBuf[0] * 256 + self._dataBuf[1]
            self._pm10 = self._dataBuf[2] * 256 + self._dataBuf[3]

            return True

        return False

    def readBlockingSensorData(self):
        self._pm2_5 = None
        self._pm10 = None
        while not self.readParticleMeasurement():
            time.sleep(1)
        print("PM2.5: %d ug/m3" % (self._pm2_5))
        print("PM10: %d ug/m3" % (self._pm10))

    def readStringUntil(self, terminator):
        """
        Function to start reading when the sensor is ready to transmit datas

        """
        c = self._serial.read()
        if (ord(c) == terminator):
            return True

    def readBytes(self, buffer, length, index):
        count = 0
        while (count < length):
            c = self._serial.read()
            for ch in c:
                ch = ord(c)
                if (ch < 0):
                    break
                buffer[index] = ch
                count += 1
                index += 1
        return [buffer, count]


