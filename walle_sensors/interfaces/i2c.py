import math
import time

from smbus2 import SMBus

class I2C:     
    def __init__(self): 
        self.i2c_address = None
        self.i2c = SMBus(1) 
        print("Set i2c!")

    def set_i2c_address(self, adr) -> bool: 
        self.i2c_address = adr
        return True 

    def write_register(self, reg, data):
        """Write data to a register."""
        self.i2c.write_byte_data(self, self.i2c_address, reg, data)

    def read_register(self, reg, length):
        return self.i2c.read_i2c_block_data(self.i2c_address, reg, length)
