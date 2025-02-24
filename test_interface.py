from walle_sensors.bmi import BMI
from walle_sensors.BME280 import BME280
from walle_sensors.MQ135 import MQ135
from walle_sensors.HUM1 import HUM1
import time 

print("Testing sensor at {}".format(time.time()))
print("======")

# Testing sensor

imu = BMI(0x69)
imu.setup()

mq = MQ135(0)
mq.setup()

hum = HUM1(1)
hum.setup()

bme = BME280(0x76)
bme.setup()

while(True):

    print("BMI reading..")
    measure = bmi.read()
    if bmi.available == False:
        print("No available data in bmi. Please check connections")
        time.sleep(0.1)
    else:
        print(measure)


    print("MQ135 reading..")
    measure = mq.read()
    if mq.available == False:
        print("No available data in mq135. Please check connections")
        time.sleep(0.1)
    else:
        print(measure)


    print("BME280 reading..")
    measure = bme.read()
    if bme.available == False:
        print("No available data in bme280. Please check connections")
        time.sleep(0.1)
    else:
        print(measure)


    print("HUM1 reading..")
    measure = hum.read()
    if hum.available == False:
        print("No available data in hum1. Please check connections")
        time.sleep(0.1)
    else:
        print(measure)
