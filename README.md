# Receiving Things Network Messages on Mosquitto using Node-Red

Used to publish a Things Network uplink message to a mqtt topic.
## Installing Packages

### Things Network Node-Red Node

A guide for installing the package using npm is available on https://www.npmjs.com/package/node-red-contrib-ttn

### Mosquitto MQTT broker

A guide for installing the Mosquitto MQTT broker can be found here: https://mosquitto.org/download/

## Setup Flows

* Start and open node-red
* Drag the ttn-uplink node onto the flow
* Connect this to a debug node to print incoming messages to the debug panel
* Add another connection to the mqtt out node (renamed airData in this case)

![Sample Flows](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/nodeRed.png)

## Configuring Nodes

### Things Network Uplink

* Under App select 'add new ttn app'
* Set the Discovery Address to: discovery.thethingsnetwork.org:1900
* Input your App ID
* Input your Access Key
* Save and input your Device ID

![Configuring uplink node](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/uplinkNode.png)
![Configuring ttn app](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/ttnappnode.png)

### MQTT Broker Node

* Under server select 'add new mqtt broker'
* Enter your mqtt server address (in my case localhost) and port (1883)
* Click update
* Choose the topic you wish to publish to (in this case airData)

![mqtt-broker node setup](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/mqttOut.png)

![mqtt-broker node setup](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/brokerNode.png)

## Testing

Open a terminal or other command-line interface and listen on a topic:

```

$ mosquitto_sub -t "INSERT TOPIC"

```

For my purposes this was the airData topic

![Terminal Response](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/mosquittoCLI.png)



