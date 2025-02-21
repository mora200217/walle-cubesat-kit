import board
import numpy as np

from walle_sensors.sensor import Sensor
from adafruit_bme280 import basic as adafruit_bme280


class BME280(Sensor):
    def __init__(self, addr):
        super().__init__()
        i2c = board.I2C()
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,addr)


    def setup(self) -> bool:
        self.units = ["°C",'%',"hPa"]
        print("--Sensor BME280 ok--")
        return True

    def read(self) -> np.array:
        return np.array([bme280.temperature, bme280.humidity, bme280.pressure])

    def available(self):
        return True

