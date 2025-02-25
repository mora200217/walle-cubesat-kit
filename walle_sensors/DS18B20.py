import os
import glob
import time
from sensor import Sensor


class DS18B20(Sensor):
    def __init__(self, addr):
        super().__init__()
        self.units = "°C"
        self.available = True
        self.addr = addr
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        self.device_file = base_dir + addr + '/w1_slave'

    def read(self):
        self.available = True

        try:
            lines = self.__read_temp_raw()
        except Exception as e:
            self.available = False
            print(f"Sensor {self.addr} no conectado - Error: {e}")
            return None

        while lines[0].strip()[-3:] != 'YES':
            print("--Mala lectura--")
            time.sleep(0.2)
            lines = self.__read_temp_raw()

        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
        return temp_c


    def __read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines





