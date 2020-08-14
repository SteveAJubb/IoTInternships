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

1. Start grafana 
> sudo service grafana-server start
2. Access grafana from your browser 
> http://localhost:8086/login
3. Enter Username and password (Initially both set to admin)
4. Change password
5. Choose Influxdb as default data source.
6. Now you can create a dashboard, add panels and visualize your data appropriately.

## Connecting LORA32u4 II to TTN

Now that the backend successfully works, we need to connect a LORA node to The Things Network, publish onto the broker to store and display the data.

### Register TTN Device

1. First you will need to create an application on The Things Network by following [these instructions] (https://www.thethingsnetwork.org/docs/applications/add.html)
2. Then you will need to register a device by following [this](https://www.thethingsnetwork.org/docs/devices/registration.html), ensure you are using OTAA due to the lack of sufficient security ABP provides.

### Adafruit Feather 32u4 II

Now that the application and device have been setup, we need to configure the Hardware and IDE. This Adafruit Feather board is a standalone board which uses the Arduino IDE. It has a LORA radio tranciever as well as an ATMEGA32 on board.

1. Open the Arduino IDE and go to the Boards manager, Install 'Adafruit AVR Boards'.
2. Open the library manager and install the MCCI LMIC Library.
3. Connect the board to your PC using a micro USB cable (make sure the cable has data lines and isnt power only).
4. Now we must map the pins of the LORA chip to the board pins. So we should connect pin 6 to DIO 1 as shown in the following diagram:

<img src="Wiring/Adafruit-Feather.png" width="300" >

**The connection of this pin is required for LMIC and for the onEvent() function signaling of EV_TXCOMPLETE to be triggered/fired, otherwise the onEvent() funciton is never called.**

> const lmic_pinmap lmic_pins = {
    .nss = 8,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 4,
    .dio = {7, 6 , LMIC_UNUSED_PIN}
};

5. Run the OTAA script on the board.


