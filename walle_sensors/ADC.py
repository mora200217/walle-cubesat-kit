import board

spi = spidev.SpiDev()
spi.open(0, 0)

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1] & 3) << 8) + r[2]
    return adc_out


def get_gas_ppm(Rs, R0):
    ratio = Rs / R0
    if ratio <= 0:
        return None
    a = 116.6020682
    b = 2.769034857
    ppm = a * (ratio ** -b)
    return ppm

while True:
    reading = analog_read(0)
    voltage = reading * 5 / 1024
    print("Reading=%d\tVoltage=%f" % (reading, voltage))
    time.sleep(1)
