from walle_sensors.bmi import BMI
from walle_sensors.BME280 import BME280
from walle_sensors.MQ135 import MQ135
import time 

print("Testing sensor at {}".format(time.time()))
print("======")

# Testing sensor
"""
imu = BMI(0x69)
imu.setup()
"""
mq = MQ135(0)
mq.setup()

bme = BME280(0x76)
bme.setup()

while(True):
    """
    time.sleep(0.2)
    if imu.available():
        print("BME280 reading..")
        print(imu.read())
    else: 
        print("No available data in imu. Please check connections")
        time.sleep(0.1)
"""

    if mq.available():
        print("MQ135 reading..")
        print(mq.read())
    else:
        print("No available data in mq. Please check connections")
        time.sleep(0.1)

    if bme.available():
        print("BME280 reading..")
        print(bme.read())
    else:
        print("No available data in bme. Please check connections")
        time.sleep(0.1)
