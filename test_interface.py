from walle_sensors.bmi import BMI

import time 

print("Testing sensor at {}".format(time.time()))
print("======")

# Testing sensor
imu = BMI(0x69)
imu.setup()

bme = BME280(0x76)
bme.setup()

while(True):
    time.sleep(100)
    if imu.available(): 
        imu.read()
    else: 
        print("No available data in imu. Please check connections")
        time.sleep(0.1)

    if bme.available():
        bme.read()
    else:
        print("No available data in bme. Please check connections")
        time.sleep(0.1)
