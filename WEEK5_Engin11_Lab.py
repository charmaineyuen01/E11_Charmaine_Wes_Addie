# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT



import csv
import time
import busio
from digitalio import DigitalInOut, Direction, Pull

from adafruit_pm25.i2c import PM25_I2C

import adafruit_bme680
import board
import numpy as np
import pandas as pd
import sys

reset_pin = None
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

def read_bme680():
    """Return BME680 dict."""
    return {
        'temperature_c': bme680.temperature,
        'gas_ohms':      bme680.gas,
        'humidity_pct':  bme680.relative_humidity,
        'pressure_hpa':  bme680.pressure,
        'altitude_m':    bme680.altitude,
    }



arguments = sys.argv
runtime = int(arguments[2])
data_path = 'data/lab5_trial' + arguments[1]

file = open(data_path, 'w', newline = None)

csvwriter = csv.writer(file, delimiter = ',')

meta = ['time', "pm10 standard", "pm25 standard", "pm100 standard",
        "pm10 env", "pm25 env", "pm100 env",
        '03um', '05um', '10um', '25um', '50um', '100um', 'temp', 'gas', 'humidity' , 'pressure' , 'altitude']

csvwriter.writerow(meta)

start = time.time()
while time.time() < start + 300:

#for i in range(10):
    time.sleep(2)
    try:
        now = time.time()
        aq = pm25.read() 
        wx = read_bme680()
        csvwriter.writerow([now, aq['pm10 standard'],  aq['pm25 standard'],  aq['pm100 standard'],
            aq['pm10 env'],       aq['pm25 env'],        aq['pm100 env'],
            aq['particles 03um'], aq['particles 05um'],  aq['particles 10um'],
            aq['particles 25um'], aq['particles 50um'],  aq['particles 100um'],
            wx['temperature_c'],  wx['gas_ohms'],        wx['humidity_pct'],
            wx['pressure_hpa'],   wx['altitude_m']])
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

file.close()

#---------------------------------------------------------------------

