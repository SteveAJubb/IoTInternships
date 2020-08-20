import paho.mqtt.client as mqtt
import json
import re
from typing import NamedTuple 
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '10.53.195.169'               # Enter IP adress
INFLUXDB_USER = ''                  # Create username             
INFLUXDB_PASSWORD = ''              # Create Password
INFLUXDB_DATABASE = 'TTN'              # Create or enter existing database 


influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

#Class to hold the recieved sensor data
class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('+/devices/+/up')
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    ergebnis = json.loads(msg.payload)
    values = ergebnis['payload_fields']
    print(values['humidity'])
 

def _parse_mqtt_message(topic, payload):
    match = re.match('([^/]+)/devices/([^/]+)/up', '+/devices/+/up')
    if match:
        location = match.group(1)
        measurement = match.group(2)
        if measurement == 'status':
            return None
        return SensorData(location, measurement, float(payload))
    else:
        return None


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


def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)


def main():
    _init_influxdb_database()

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.tls_set()
mqtt_client.username_pw_set('indoor-air-quality',password='ttn-account-v2.gtxNrMTOvSfWmK4ad2ZJf3VJkk91bREYKXmEfc2WvLg')
 
mqtt_client.connect('eu.thethings.network', 8883, 60)
 
mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
