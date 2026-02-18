# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT



import csv
import time
#import numpy as np
"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""



import board
import busio
from digitalio import DigitalInOut, Direction, Pull

from adafruit_pm25.i2c import PM25_I2C

import adafruit_bme680
import board
import numpy as np
import pandas as pd

reset_pin = None
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

file = open('data/lab4data.csv', 'w', newline = None)

csvwriter = csv.writer(file, delimiter = ',')

meta = ['time', "pm10 standard", "pm25 standard", "pm100 standard",
        "pm10 env", "pm25 env", "pm100 env",
        '03um', '05um', '10um', '25um', '50um', '100um']

csvwriter.writerow(meta)



for i in range(10):
    time.sleep(2)
    try:
        now = time.time()
        aqdata = pm25.read()
        csvwriter.writerow([now, aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"],
                            aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"],
                            aqdata["particles 03um"], aqdata["particles 05um"], aqdata["particles 10um"], 
                            aqdata["particles 25um"], aqdata["particles 50um"], aqdata["particles 100um"]])
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

file.close()

#---------------------------------------------------------------------
# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

timeout = 10
start_time = time.time()

temp = []
gas = []
humidity = []
pressure = []
alt = []
current_time = []

while True:
    temp = np.append(temp, bme680.temperature)
    gas = np.append(gas, bme680.gas)
    humidity = np.append(humidity, bme680.relative_humidity)
    pressure = np.append(pressure, bme680.pressure)
    alt = np.append(alt, bme680.altitude)
    current_time = np.append(current_time, time.ctime())
    
    if (time.time() - start_time) > timeout:
        print("END OF LOOP")
        break
    
    time.sleep(2)

    
df = pd.DataFrame({'Time': current_time, 'Temp': temp, 'Gas': gas, 'Humidity': humidity, 'Pressue': pressure , 'Alt': alt})
print(df)

df.to_csv('ENGIN11_Week3Lab.csv')
