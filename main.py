from smbus2 import SMBus
import math
import time

# Constants
BMI160_I2C_ADDR = 0x69
ACCEL_SENSITIVITY = 16384.0  # ±2g sensitivity for the accelerometer in LSB/g

# Initialize I2C with SMBus (Raspberry Pi uses SMBus for I2C)
i2c = SMBus(1)  # Bus 1 is the standard for Raspberry Pi 4

def write_register(addr, reg, data):
    """Write data to a register."""
    i2c.write_byte_data(addr, reg, data)

def read_register(addr, reg, length):
    """Read data from a register."""
    return i2c.read_i2c_block_data(addr, reg, length)

def initialize_bmi160():
    """Initialize the BMI160 sensor."""
    write_register(BMI160_I2C_ADDR, 0x7E, 0x11)  # ACC_NORMAL_MODE
    time.sleep(0.1)

def read_raw_acceleration():
    """Read raw acceleration data."""
    data = read_register(BMI160_I2C_ADDR, 0x12, 6)  # Read accel data
    ax_raw = int.from_bytes(data[0:2], 'little', signed=True)
    ay_raw = int.from_bytes(data[2:4], 'little', signed=True)
    az_raw = int.from_bytes(data[4:6], 'little', signed=True)
    return ax_raw, ay_raw, az_raw

def auto_calibrate():
    """Perform auto-calibration to remove noise or error."""
    print("Starting auto-calibration...")
    num_samples = 100
    ax_offset, ay_offset, az_offset = 0, 0, 0

    for _ in range(num_samples):
        ax_raw, ay_raw, az_raw = read_raw_acceleration()
        ax_offset += ax_raw
        ay_offset += ay_raw
        az_offset += az_raw
        time.sleep(0.01)

    ax_offset //= num_samples
    ay_offset //= num_samples
    az_offset //= num_samples
    az_offset -= int(ACCEL_SENSITIVITY)  # Adjust for gravity

    print(f"Offsets - X: {ax_offset}, Y: {ay_offset}, Z: {az_offset}")
    return ax_offset, ay_offset, az_offset

def read_acceleration(ax_offset, ay_offset, az_offset):
    """Read acceleration data, apply offsets, and convert to m/s²."""
    ax_raw, ay_raw, az_raw = read_raw_acceleration()
    ax = ((ax_raw - ax_offset) / ACCEL_SENSITIVITY) * 9.81
    ay = ((ay_raw - ay_offset) / ACCEL_SENSITIVITY) * 9.81
    az = ((az_raw - az_offset) / ACCEL_SENSITIVITY) * 9.81
    return ax, ay, az

def calculate_tilt_angles(ax, ay, az):
    """Calculate pitch and roll angles from acceleration."""
    pitch = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 180.0 / math.pi
    roll = math.atan2(-ax, az) * 180.0 / math.pi
    return pitch, roll

# Initialize BMI160
initialize_bmi160()
print("BMI160 Initialized")

# Perform auto-calibration
ax_offset, ay_offset, az_offset = auto_calibrate()

while True:
    try:
        ax, ay, az = read_acceleration(ax_offset, ay_offset, az_offset)
        pitch, roll = calculate_tilt_angles(ax, ay, az)

        print(f"Acceleration (m/s²): X: {ax:.2f}, Y: {ay:.2f}, Z: {az:.2f}")
        print(f"Tilt Angles: Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")
        print("=" * 50)

    except OSError as e:
        print("I2C Error:", e)

    time.sleep(0.1)

