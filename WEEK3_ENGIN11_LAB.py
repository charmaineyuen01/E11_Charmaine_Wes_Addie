
import adafruit_bme680
import time
import board
import numpy as np
import pandas as pd

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
