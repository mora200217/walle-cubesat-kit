import board
import numpy as np

from walle_sensors.sensor import Sensor
from adafruit_bme280 import basic as adafruit_bme280


class BME280(Sensor):
    def __init__(self, addr):
        super().__init__()

        self.units = ["°C", '%', "hPa"]

        i2c = board.I2C()

        self.available = True

        try:
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,addr)
        except Exception as e:
            self.available = False
            print(f"Error: Sensor BME280 no conectado - {e}")




    def setup(self) -> bool:
        print("--Sensor BME280 ok--")
        return True


    def read(self) -> np.array:

        self.available = True

        try:

            return np.array([self.bme280.temperature, self.bme280.humidity, self.bme280.pressure])

        except OSError as e:

            self.available = False
            print(" -!- Sensor BME280 desconectado -!-")
            return np.array([None, None, None])

        except Exception as e:

            self.available = False
            print(f" -!- Error inesperado en BME280: {e} -!-")
            return np.array([None, None, None])



