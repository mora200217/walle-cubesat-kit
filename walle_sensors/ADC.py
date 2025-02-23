import spidev
import time

# Inicializar SPI

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):

    if channel < 0 or channel > 7:
        raise ValueError("El canal debe estar entre 0 y 7")

    # Enviar comando de lectura: 1 byte de inicio, 3 bits de selección, 5 bits de relleno
    command = [1, (8 + channel) << 4, 0]
    response = spi.xfer2(command)

    # Procesar respuesta (10 bits)
    result = ((response[1] & 3) << 8) + response[2]
    return result

try:
    while True:
        valor = read_adc(0)  # Leer canal 0
        voltaje = (valor * 3.3) / 1023  # Convertir a voltaje (3.3V referencia)
        print(f"Valor ADC: {valor}, Voltaje: {voltaje:.2f}V")
        time.sleep(1)

except KeyboardInterrupt:
    print("Cerrando SPI")
    spi.close()
