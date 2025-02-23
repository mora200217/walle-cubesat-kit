from walle_sensors.interfaces.spi import SPI
from walle_sensors.sensor import Sensor


class MQ135(SPI, Sensor):
    def __init__(self, canal):
        super().__init__()
        self.canal = canal
        self.disponible = True

    def setup(self) -> bool:
        print("--Sensor MQ135 ok--")
        return True

    def read(self):

        command = [1, (8 + self.canal) << 4, 0]
        response = self.spi.xfer2(command)
        result = ((response[1] & 3) << 8) + response[2]
        voltage = (result * 5.24) / 1023

        if voltage <= 0:
            self.disponible = False
            return None
        self.disponible = True

        return self.get_gas_ppm(voltage)

    def available(self):
        self.read()
        return self.disponible


    def get_gas_ppm(self, Vout):
        Vc = 5.24
        RL = 1000 #-- 1k --
        R0 = 7000 #-- 7k --

        Rs = ((Vc - Vout) / Vout) * RL

        ratio = Rs / R0

        a = 116.6020682
        b = 2.769034857
        ppm = a * (ratio ** -b)
        return ppm



