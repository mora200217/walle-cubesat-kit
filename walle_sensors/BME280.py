import board
import numpy as np

from walle_sensors.sensor import Sensor
from adafruit_bme280 import basic as adafruit_bme280


class BME280(Sensor):
    def __init__(self, addr):
        super().__init__()

        self.units = ["°C", '%', "hPa"]

        i2c = board.I2C()

        try:
            self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,addr)
        except Exception as e:
            print(f"Error: Sensor BME280 no conectado - {e}")  # Mensaje de error opcional


    def setup(self) -> bool:
        print("--Sensor BME280 ok--")
        return True

    def read(self) -> np.array:
        return np.array([self.bme280.temperature, self.bme280.humidity, self.bme280.pressure])

    def available(self):
        try:
            _ = self.bme280.temperature  # Intenta leer un valor del sensor
            return True
        except Exception as e:
            print(f"Error: Sensor desconectado - {e}")  # Mensaje de error opcional
            return False

