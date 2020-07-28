# This script is used to build subscribe to MQTT broker
# and publish the sensor data onto an influx database


# Import re, MQTT and Influx clients
import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

# Initialise parameters
INFLUXDB_ADDRESS = ''               # Enter IP adress
INFLUXDB_USER = ''                  # Create username             
INFLUXDB_PASSWORD = ''              # Create Password
INFLUXDB_DATABASE = ''              # Create or enter existing database

MQTT_ADDRESS = 'test.mqtt.org'      # Enter MQTT server address (public or private)
MQTT_USER = ''                      # Create MQTT Username
MQTT_PASSWORD = '12345'             # Create MQTT password
MQTT_TOPIC = 'home/+/+'             # Enter topic name
MQTT_REGEX = 'home/([^/]+)/([^/]+)' 
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge' 

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

#Class to hold the recieved sensor data
class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float
 

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

# Execute when message is recieved
def on_message(client, userdata, msg):    
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)


def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        return SensorData(location, measurement, float(payload))
    else:
        return None

# Build an influxDB structure to store the recieved data continuosly
def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    
        
                ]
    influxdb_client.write_points(json_body)

# Create database if none have been created by this name
def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

#Call previous functions to begin connection
def main():
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
