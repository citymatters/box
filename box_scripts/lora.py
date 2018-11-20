import time
import sys
import serial
TTYADDR = "/dev/ttyS2"


class RN2XX3():
    """Microchip RN2903 and RN2483 LoRa Wireless Modules

    This class implements all the functions that are available in the
    modules for evaluation.
    """

    COMMANDS = {
        "SYS_SLEEP":b"sys sleep {}",
        "SYS_RST":b"sys reset",
        "SYS_FACRST":b"sys factoryRESET",
        "SYS_ERASEFW":b"sys eraseFW",

        "SYS_VER":b"sys get ver",
        "SYS_VDD":b"sys get vdd",
        "SYS_HWEUI":b"sys get hweui",
        "SYS_NVMAT":b"sys get nvm {}",

        "SYS_NVMSET":b"sys set nvm {} {}",
        "SYS_PINCFG":b"sys set pindig {0} {1}",

        "MAC_RSTBAND":b"mac reset {}",
        "MAC_TX":b"mac tx {0} {1} {2}",
        "MAC_SAVE":b"mac save",
        "MAC_PAUSE":b"mac pause",
        "MAC_RESUME":b"mac resume",

        "MAC_DEVADDR":b"mac get devaddr",
        "MAC_DEVEUI":b"mac get deveui",
        "MAC_APPEUI":b"mac get appeui",
        "MAC_DR":b"mac get dr",
        "MAC_BAND":b"mac get band",
        "MAC_PWRIDX":b"mac get pwridx",
        "MAC_ADR":b"mac get adr",
        "MAC_RETX":b"mac get retx",
        "MAC_RXDELAY1":b"mac get rxdelay1",
        "MAC_RXDELAY2":b"mac get rxdelay2",
        "MAC_AR":b"mac get ar",
        "MAC_RX2":b"mac get rx2 {}",
        "MAC_DYCLEPS":b"mac get dcycleps",
        "MAC_MRGN":b"mac get mrgn",
        "MAC_GWNB":b"mac get gwnb",
        "MAC_STATUS":b"mac get status",

        "MAC_DEVADDRSET":b"mac set devaddr {}",
        "MAC_DEVEUISET":b"mac set deveui {}",
        "MAC_APPEUISET":b"mac set appeui {}",
        "MAC_NWKSKEYSET":b"mac set nwkskey {}",
        "MAC_APPSKEYSET":b"mac set appskey {}",
        "MAC_PWRIDXSET":b"mac set pwridx {}",
        "MAC_DRSET":b"mac set dr {}",
        "MAC_ADRSET":b"mac set adr {}",
        "MAC_BATSET":b"mac set bat {}",
        "MAC_RETXSET":b"mac set retx {}",
        "MAC_LINKCHKSET":b"mac set linkchk {}",
        "MAC_RXDELAY1SET":b"mac set rxdelay1 {}",
        "MAC_ARSET":b"mac set ar {}",
        "MAC_RXSET":b"mac set rx2 {0} {1}",
        "MAC_JOIN_OTA":b"mac join otaa",

    }


    def __init__(self, ser=None, verbose=False):
        self.verbose = verbose
        self.ser = ser
        if self.ser == None:
            raise ValueError('No valid serial port')
        # execute reset of the module by pulling down a pin
        if sys.platform == "pyboard":
            RN_RESET_PIN = pyb.Pin(pyb.Pin.cpu.A5, mode=pyb.Pin.OUT_PP)
            RN_RESET_PIN.value(1)
            time.sleep(0.25)
            RN_RESET_PIN.value(0)
            time.sleep(0.25)
            RN_RESET_PIN.value(1)

    def getConn(self):
        return self.ser

    def closeConn(self):
        if not sys.platform == "pyboard":
            self.ser.close()
        else:
            self.ser.deinit()

    def execCmd(self, cmd):
        print(type(cmd))
        #if self.verbose:
        #    print("Attempting to execute command: {}\r\n".format(cmd))

        if isinstance(cmd, str):
            print("convert string to byte")
            cmd1 = cmd.encode()
            command = cmd1 + str.encode("\r\n")
        else:
            print("type of cmd : {}".format(type(cmd)))
            command = cmd+ str.encode("\r\n")
        if self.verbose:
            print("Attempting to execute command: {}\r\n".format(cmd))

        self.ser.write(command)
        #self.ser.write("\r\n")
        line = self.ser.readline()
        if self.verbose:
            print("Command response: {}\r\n".format(line))
        return line.decode("utf-8", errors="ignore")
        if self.verbose:
            print("Attempting to execute command: {}\r\n".format(cmd))

    # SYS COMMANDS

    def getSysVersion(self):
        return self.execCmd(self.COMMANDS["SYS_VER"])

    def getSysVdd(self):
        return self.execCmd(self.COMMANDS["SYS_VDD"])

    def getSysHweui(self):
        return self.execCmd(self.COMMANDS["SYS_HWEUI"])

    def getSysNvmAt(self, nvmaddr):
        return self.execCmd(self.COMMANDS["SYS_NVMAT"].format(nvmaddr))

    def setSysNvmAg(self, nvmaddr, hexByte):
        return self.execCmd(self.COMMANDS["SYS_NVMSET"].decode("utf-8", errors="ignore").format(nvmaddr, hexByte))

    def sysSleep(self, millis):
        return self.execCmd(self.COMMANDS["SYS_SLEEP"].decode("utf-8", errors="ignore").format(millis))

    def set_appkey(self):
        return self.execCmd("mac set appkey 6C91EAC6162C10CBD54486D1A68A396F")

    def set_app_eui(self):
        return self.execCmd("mac set appeui 70B3D57ED0014B04")

    def sys_safe_settings(self):
        return self.execCmd(self.COMMANDS["MAC_SAVE"])

    def jion_ota(self):
        return self.execCmd(self.COMMANDS["MAC_JOIN_OTA"])

    def sysReset(self):
        return self.execCmd(self.COMMANDS["SYS_RST"])

    def send_data_to_network(self):
        payload = "Hello"
        cmd = "mac tx cnf 45 " + payload
        return self.execCmd(cmd)

    # MAC COMMANDS

    def getMacDeveui(self):
        return self.execCmd(self.COMMANDS["MAC_DEVEUI"])

def main():
    """ """
    ser = serial.Serial(TTYADDR, 57600, timeout=5)

    loraClient = RN2XX3(ser=ser, verbose=True)

    #print("\r\nCHIP FIRMWARE VERSION IS: {}".format(loraClient.getSysVersion() ))
    #time.sleep(1)
    #print("\r\nCHIP HARDWARE EUI IS: {}".format(loraClient.getSysHweui() ))
    #time.sleep(1)
    #print("\r\nCHIP VDD READING IS: {}".format(loraClient.getSysVdd() ))
    #time.sleep(1)
    print("\r\nCHIP MAC DEVEUI IS: {}".format(loraClient.getMacDeveui() ))
    #print("SLEEPING WITH RN2XX3 CHIP\r\n {}".format(loraClient.sysSleep(3000) ))
    #print("SETTING NVM AT 3FF TO 88: {}".format(loraClient.setSysNvmAg('3FF','88') ))
    #time.sleep(0.25)
    #print("\nNVM MEMORY VALUE AT: 3FF IS: {}".format(loraClient.getSysNvmAt('3FF')) )
    #print("RESETTING CLIENT {}".format(loraClient.sysReset()))
    #loraClient.closeConn()
    loraClient.set_appkey()
    loraClient.set_app_eui()
    loraClient.sys_safe_settings()
    loraClient.jion_ota()
    loraClient.send_data_to_network()
    loraClient.closeConn()




if __name__ == "__main__":
    main()
