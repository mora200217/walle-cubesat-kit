"""
    IMU Sensor (BMI160) 
    -
"""
import time 
import math 
import numpy as np

from walle_sensors.sensor import Sensor
from walle_sensors.interfaces.i2c import I2C
# Initialize I2C with SMBus (Raspberry Pi uses SMBus for I2C)

class BMI(I2C, Sensor): 
    def __init__(self, addr): 
        super().__init__()
        self.set_i2c_address(addr)
        self.ACCEL_SENSITIVITY = 16384.0 

        self.ax_offset = 0
        self.ay_offset = 0
        self.az_offset = 0

        self.available = True

    def setup(self) -> bool:
        self.units = "m/s^2"
        self.available = True

        try:
            self.write_register(0x7E, 0x11)  # ACC_NORMAL_MODE
            print("--Sensor BMI ok--")
        except Exception as e:
            self.available = False

        time.sleep(0.1)

        return True 
    
    def read(self) -> np.array:
        self.available = True
        try:
            return np.array(self.__read_acceleration(self.ax_offset, self.ay_offset, self.az_offset))
        except Exception as e:
            self.available = False
            print(" -!- Sensor BMI desconectado -!-")
            return np.array([None, None, None])


    def __read_raw_acceleration(self):
        """Read raw acceleration data."""
        data = self.read_register(0x12, 6)  # Read accel data
        ax_raw = int.from_bytes(data[0:2], 'little', signed=True)
        ay_raw = int.from_bytes(data[2:4], 'little', signed=True)
        az_raw = int.from_bytes(data[4:6], 'little', signed=True)
        return ax_raw, ay_raw, az_raw

    def __auto_calibrate(self):
        print("Starting auto-calibration...")
        num_samples = 100
        # self.ax_offset, self.ay_offset, self.az_offset = 0, 0, 0

        for _ in range(num_samples):
            ax_raw, ay_raw, az_raw = self.__read_raw_acceleration()
            self.ax_offset += ax_raw
            self.ay_offset += ay_raw
            self.az_offset += az_raw
            time.sleep(0.01)

        self.ax_offset //= num_samples
        self.ay_offset //= num_samples
        self.az_offset //= num_samples
        self.az_offset -= int(self.ACCEL_SENSITIVITY)  # Adjust for gravity

        print(f"Offsets - X: {self.ax_offset}, Y: {self.ay_offset}, Z: {self.az_offset}")
        return self.ax_offset, self.ay_offset, self.az_offset

    def __read_acceleration(self, ax_offset, ay_offset, az_offset):
        """Read acceleration data, apply offsets, and convert to m/s²."""
        ax_raw, ay_raw, az_raw = self.__read_raw_acceleration()
        ax = ((ax_raw - self.ax_offset) / self.ACCEL_SENSITIVITY) * 9.81
        ay = ((ay_raw - self.ay_offset) / self.ACCEL_SENSITIVITY) * 9.81
        az = ((az_raw - self.az_offset) / self.ACCEL_SENSITIVITY) * 9.81
        return ax, ay, az

    def __calculate_tilt_angles(self, ax, ay, az):
        """Calculate pitch and roll angles from acceleration."""
        pitch = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 180.0 / math.pi
        roll = math.atan2(-ax, az) * 180.0 / math.pi
        return pitch, roll



