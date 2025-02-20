from walle_sensors.bmi import BMI

import time 

print("Testing sensor at {}".format(time.time()))
print("======")

# Testing sensor
imu = BMI(0x69)
imu.setup()

while(True): 
    if imu.available(): 
        imu.read()
    else: 
        print("No available data. Please check connections")
        time.sleep(0.1)
