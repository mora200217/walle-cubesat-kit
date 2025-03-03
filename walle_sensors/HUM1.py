import RPi.GPIO as GPIO
from walle_sensors.interfaces.spi import SPI
from walle_sensors.sensor import Sensor


class HUM1(SPI, Sensor):
    def __init__(self, canal):
        super().__init__()
        self.canal = canal
        self.available = True

        CS_PIN = 15

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CS_PIN, GPIO.OUT)
        GPIO.output(CS_PIN, GPIO.HIGH)

    def setup(self) -> bool:
        print("--Sensor de humadad ok--")
        return True

    def read(self):
        self.available = True

        GPIO.output(CS_PIN, GPIO.LOW)
        command = [1, (8 + self.canal) << 4, 0]
        response = self.spi.xfer2(command)
        GPIO.output(CS_PIN, GPIO.HIGH)

        result = ((response[1] & 3) << 8) + response[2]
        humedad = (result * 100) / 1023

        if humedad <= 0:
            self.available = False
            return None


        return humedad
