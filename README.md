# Transferring Data From the Things Network to InfluxDB

## Installation

### Node-Red

Before installing Node-Red you will first need to install:
* Node.js: https://nodejs.org/en/download/ (although I used this guide for Ubuntu: https://tecadmin.net/install-latest-nodejs-npm-on-ubuntu/)
* Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Node-Red can then be installed and run locally using: https://nodered.org/docs/getting-started/local

#### Things Network Node-Red Node

A guide for installing the package using npm is available on https://www.npmjs.com/package/node-red-contrib-ttn'

### InfluxDB

Influx provides a general downloads page that should work for any system: https://portal.influxdata.com/downloads/
However, I found it simple to install on Ubuntu using this guide: https://websiteforstudents.com/how-to-install-influxdb-on-ubuntu-18-04-16-04/

## Usage

### InfluxDB

To access the InfluxDB server from the command line use:

```

$ influx

```
It uses similar syntax to SQL. Ex:

```

> CREATE DATABASE <DATABASE NAME>
> USE <DATABASE NAME>

```

One important thing to note is that data of a similar type is linked through a shared 'measurement' (specified when inputting the infomation to InfluxDB in whatever way). Measurements usually contain data fields and classification tags. Ex:

```

> SELECT <field> FROM <measurement> WHERE <tag> ...

```

Ex. When inputting data to the InfluxDB database a JSON object being inserted would be in this form:

```

   {
        "measurement": <measurement>,
        "tags": {
            "<tag1>": xxxx,
            "<tag2>": xxxx,
            ... 
        },
        "fields": {
            "<field1>": xxxx,
            "<field2>": xxxx,
            ...
        }
    }

```

### Node-Red

To start node-red open a terminal or command line and enter:

```

$ node-red

```

Then go to the webpage http://127.0.0.1:1880 in your browser. This is where you configure the node-red flows. A simple introductory guide to node-red flows can be found here: https://nodered.org/docs/tutorials/

## Setup

### InfluxDB

Before you begin entering data into Influx you need to create a database:

```

$ influx
> CREATE DATABASE <DATABASE_NAME> //Ex. ttndb

```
### Node Red

In its most basic form, the node-red flow could simply join the ttn uplink node to the InfluxDB output node. This would take the payload of the ttn uplink message (msg.payload) and input this information as fields into InfluxDB. Meaning that whenever a message is sent in, it will be piped through node-red and into InfluxDB. InfluxDB would then automatically timestamp the data and make useable in a time-series format. In practice you may want to complicate the flows by changing the message, joining it with another message, delaying messages etc. However, I would recommend always having a debug node available to print the incoming ttn uplink message to the debug panel in node-red, the allows you to see what is going on in more detail and understand things better.

![Configuring Node-Red flows](https://github.com/SteveAJubb/IoTInternships/blob/ttn_to_influx_via_nodered/flows.png)

#### Things Network Uplink Node

* Under App select 'add new ttn app'
* Set the Discovery Address to: discovery.thethingsnetwork.org:1900
* Input your App ID
* Input your Access Key
* Save and input your Device ID

![Configuring uplink node](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/uplinkNode.png)
![Configuring ttn app](https://github.com/seth20012/practiceIoT/blob/ttn_to_mqtt/ttnappnode.png)

More information about the Things Network node can be found here: https://github.com/TheThingsNetwork/nodered-app-node/blob/HEAD/docs/quickstart.md

#### InfluxDB Output Node

Information about installing and seting up the node can be found here: https://www.thethingsnetwork.org/labs/story/store-and-visualize-data-using-influxdb-and-grafana/ under 'Setup InfluxDB node on Node-Red'. This also provides a brief example setup using an InfluxDB database named ttndb. 

In my case I have created a database in InfluxDB called trackmap, replace this in the database input box as you configure the node. I have also specified the 'measurement' (carTrack) that I want the data to be classified under by InfluxDB. By specifying a 'measurement' for the information coming in, this greatly helps InfluxDB to access and categorise that data later on. The measurement could be anything but should preferably be something that relates to what you are measuring, Ex. location, airQuality... I have also provided a username and password for InfluxDB; however, by default InfluxDB is not password protected so it can be left blank.

![Influx Node](https://github.com/SteveAJubb/IoTInternships/blob/ttn_to_influx_via_node_red/influx_out.png)
![Influx Config](https://github.com/SteveAJubb/IoTInternships/blob/ttn_to_influx_via_node_red/influx_node_config.png)



## Viewing the Information

If you follow the earlier guide (https://www.thethingsnetwork.org/labs/story/store-and-visualize-data-using-influxdb-and-grafana/), it should introduce how to link InfluxDB and Grafana. However, if you just want to check that the information has been stored correctly you can use the influx shell:

```

$ influx
> SELECT * FROM <MEASUREMENT>

```


