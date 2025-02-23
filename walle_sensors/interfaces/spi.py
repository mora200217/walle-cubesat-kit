import spidev

class SPI:
    def __init__(self):
        self.a = 1
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1350000
        print("Set spi!")
