# This script is used to retrieve sensor data from The Things Network Console
# and publish it onto an mqtt broker
# Whenever data is published to the broker, it is stored in influx


import paho.mqtt.client as mqtt
import json
import re
from typing import NamedTuple 
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = ''                       # Enter IP adress
INFLUXDB_USER = ''                          # Create username             
INFLUXDB_PASSWORD = ''                      # Create Password
INFLUXDB_DATABASE = ''                      # Create or enter existing database 


MQTT_USER = 'indoor-air-quality'
MQTT_PASSWORD = 'ttn-account-v2.gtxNrMTOvSfWmK4ad2ZJf3VJkk91bREYKXmEfc2WvLg'
MQTT_ADDRESS = 'eu.thethings.network'
# Setting up the Influx server
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('+/devices/+/up')       # subscribe to topic
 
# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg):
    ergebnis = json.loads(msg.payload)
    values = ergebnis['payload_fields']
    temp = values['temperature']            # 'temperature' is a part of the decoded payload data on TTN console  
    print(temp)
    
    _send_sensor_data_to_influxdb(temp)        



# Building database structure is calledback when data recieved
def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': 'Temperature',
            'tags': {
                'location': 'Lab'
            },
            'fields': {
                'value': sensor_data
            }
        }
    
        
               
                ]
    influxdb_client.write_points(json_body)


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

# Main function
def main():

    _init_influxdb_database()

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.tls_set()
    mqtt_client.username_pw_set(MQTT_USER,password = MQTT_PASSWORD) 
 
    mqtt_client.connect(MQTT_ADDRESS, 8883, 60)
 
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
