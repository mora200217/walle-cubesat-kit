from walle_sensors.bmi import BMI
from walle_sensors.BME280 import BME280

import time 

print("Testing sensor at {}".format(time.time()))
print("======")

# Testing sensor
imu = BMI(0x69)
imu.setup()

bme = BME280(0x76)
bme.setup()

while(True):
    time.sleep(0.2)
    if imu.available(): 
        imu.read()
    else: 
        print("No available data in imu. Please check connections")
        time.sleep(0.1)

    if bme.available():
        print("Reading..")
        print(bme.read())
    else:
        print("\r Volver a intentar conexión en 3 segundos...")
        time.sleep(3)
