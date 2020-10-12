# Note that this is only useful for very specific applications. The Things Network can directly connect to MQTT without node-red. I use node-red to access the data and then pass it to MQTT making this application a bit redundant.

# Receiving Things Network Messages on Mosquitto using Node-Red

Used to publish a Things Network uplink message to a mqtt topic.
## Installing Packages

### Installing Node-Red

Before installing Node-Red you will first need to install:
* Node.js: https://nodejs.org/en/download/ (although I used this guide for Ubuntu: https://tecadmin.net/install-latest-nodejs-npm-on-ubuntu/)
* Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Node-Red can then be installed and run locally using: https://nodered.org/docs/getting-started/local

#### Things Network Node-Red Node

A guide for installing the package using npm is available on https://www.npmjs.com/package/node-red-contrib-ttn

### Mosquitto MQTT broker

A guide for installing the Mosquitto MQTT broker can be found here: https://mosquitto.org/download/

## Setup Flows

To start node-red open a terminal or command line and enter:

```

$ node-red

```

Then go to the webpage http://127.0.0.1:1880 in your browser. This is where you configure the node-red flows. A simple introductory guide to node-red flows can be found here: https://nodered.org/docs/tutorials/

![Sample Flows](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/nodeRed.png)

* Start and open node-red
* Drag the ttn-uplink node onto the flow
* Connect this to a debug node to print incoming messages to the debug panel
* Add another connection to the mqtt out node (renamed airData in this case)

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



