# IOT Temperature Monitoring Application

The aim is to connect a LORA node to The Things network, retrieve the data using an MQTT broker on a raspberry pi, storing it in an influx database, and displaying the data on a Grafan dashboard.

## Testing MQTT, InfluxDB and Grafana 

You can follow the steps provided in [this](https://mosquitto.org/download/) link to install the Mosquitto MQTT broker.

- Start running the broker using:
> sudo systemctl enable mosquitto
- Check the broker is successfully running using:
> sudo systemctl status mosquitto


Docker is an easy way to install Influxdb and Grafana on your raspberry pi. Follow the instructions in [this](https://www.docker.com/blog/happy-pi-day-docker-raspberry-pi/) link up until number 6. Then go ahead and install [Influxdb](https://hub.docker.com/_/influxdb) and [Grafana](https://hub.docker.com/r/grafana/grafana).

**Install the following python clients on your machine:**

- paho-mqtt
> sudo pip3 install paho-mqtt
- Influxdb
> sudo pip3 install influxdb

### Testing Hardware 

In order to test the previous setup, an ESP 8266 standalone board and a temperature sensor have been used to publish the temperature data to the MQTT broker. 

The following diagram displays the board and wiring confiugration used:

<img src="Wiring/ESP8266.png" width="300" >

The Arduino sketch SendSensorData.ino uses this board to relay the data over wifi and MQTT. (Correct board configuration for the ESP8266 and libraries must be used.)

The python script InfluxdbSetup.py must be ran on the raspberry pi to listen and store the data on influxdb.


### Dashboard Display

1. start grafana 
> sudo service grafana-server start
2. Access grafana from your browser 
> http://localhost:8086/login
3. Enter Username and password (Initially both set to admin)
4. Change password
5. Choose Influxdb as default data source.
6. Now you can create a dashboard, add panels and visualize your data appropriately.

