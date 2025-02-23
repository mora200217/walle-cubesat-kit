from walle_sensors.interfaces.spi import SPI
from walle_sensors.sensor import Sensor


class MQ135(Sensor, SPI):

    def __init__(self, canal):
        super().__init__()
        self.canal = canal

    def setup(self) -> bool:
        print("--Sensor MQ135 ok--")
        return True

    def read(self):

        command = [1, (8 + self.canal) << 4, 0]
        response = self.spi.xfer2(command)
        result = ((response[1] & 3) << 8) + response[2]
        Voltage = (result * 5) / 1023

        #return self.get_gas_ppm(Voltage)
        return Voltage
    def available(self):
        return True


    def get_gas_ppm(Vout):
        Vc = 5
        RL = 1000 #-- 1k --
        R0 = 7000 #-- 7k --

        if Vout <= 0:
            Rs = -1
            pass
        else:
            Rs = ((Vc - Vout) / Vout) * RL


        ratio = Rs / R0

        if ratio <= 0:
            return None

        a = 116.6020682
        b = 2.769034857
        ppm = a * (ratio ** -b)
        return ppm



