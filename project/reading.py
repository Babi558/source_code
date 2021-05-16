from os import stat
import serial
import time
import datetime
from pymongo import MongoClient
from pymongo import ReturnDocument
import datetime
import random
from flask import Flask, render_template
app = Flask(__name__)


# config
#serial_port = '/dev/cu.usbmodem141101'
serial_port = 'COM5'
mongodb_host = 'localhost'
mongodb_db = 'farm'
temperature_location = "phase1"
temperature_location1 = "phase2"
temperature_location2 = "phase3"

# Connect to MongoDB
client = MongoClient(mongodb_host, 27017)

db = client[mongodb_db]
collection = db['data']

current = db['current']
current.delete_many({})

current_obj = [
    {"_id": 1, "moisture": 0.0, "temperature": 0.0, "humidity": 0, "status": 'N/A', 'datetime': datetime.datetime.now(),
     'location': temperature_location},
    {"_id": 2, "moisture": 0.0, "temperature": 0.0, "humidity": 0, "status": 'N/A', 'datetime': datetime.datetime.now(),
     'location': temperature_location1},
    {"_id": 3, "moisture": 0.0, "temperature": 0.0, "humidity": 0, "status": 'N/A', 'datetime': datetime.datetime.now(),
     'location': temperature_location2}
]
current.insert_many(current_obj)


# Read from serial
ser = serial.Serial(serial_port, 9600, timeout=0)
fixed_interval = 10

while 1:
    try:
        value = ser.readline().split()
        temperature_c = humidity = moisture = 0
        # If we received a measurement, print it and send it to MongoDB.
        if len(value) == 4:
            moisture = int(value[0])
            temperature_c = float(value[1])
            humidity = float(value[2])
            status = str(value[3]).replace('b', '').replace("\'", '')
            # Data for analysis
            temp = [temperature_location,
                    temperature_location1, temperature_location2]
            selection = random.choice(temp)
            current.find_one_and_update({'location': selection},
                                        {'$set': {'temperature': temperature_c,
                                                  'humidity': humidity,
                                                  'moisture': moisture,
                                                  'status': status,
                                                  'datetime': datetime.datetime.now(), }},
                                        return_document=ReturnDocument.AFTER)
            collection.insert_one(
                {
                    'temperature': temperature_c,
                    'humidity': humidity,
                    'moisture': moisture,
                    'status': status,
                    'datetime': datetime.datetime.now(),
                    'location': selection}
            )

            print(temperature_c, humidity, moisture,
                  status, selection)
    except serial.SerialTimeoutException:
        print('Error! Could not read the Temperature Value from unit')
    except ValueError:
        print('Error! Could not convert temperature to float')
    finally:
        time.sleep(fixed_interval)
