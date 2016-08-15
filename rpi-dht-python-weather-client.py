#!/usr/bin/python

import sys
import Adafruit_DHT
from influxdb import InfluxDBClient

sensor = Adafruit_DHT.AM2302
pin = 18

humidity, temperatureC = Adafruit_DHT.read_retry(sensor, pin)
temperatureF = temperatureC * 9/5.0 + 32

if humidity is not None and temperatureC is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperatureF, humidity))
    inClient = InfluxDBClient(host='192.168.1.245', port=8086, username='sensor2', password='s1mple', database='weather')
    data = [
      {
        "measurement": "temperature",
        "tags": {
          "sensor": "sensor2"
        },
        "fields": {
          "Celcius": temperatureC,
          "Fahrenheit": temperatureF
        }
      },
      {
        "measurement": "relative_humidity",
        "tags": {
          "sensor": "sensor2"
        },
        "fields": {
          "rh": humidity
        }
      }
    ]
    inClient.write_points(data)

else:
    print('Failed to get reading. Try again!')
    sys.exit(1)

