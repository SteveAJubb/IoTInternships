# Visualising Data on Grafana via Node-RED and InfluxDB
**For data from The Things Network**
- Retrieve Using Node-RED
- Store in a Database on InfluxDB
- Query and Visualise onto a Dashboard Using Grafana
## Node-RED
The need to manipulate sensor data from The Things Network (TTN) before storing in a database was the main motivator for using Node-RED. In this given case, data from an industrial air monitoring sensor in its original format could not be stored in InfluxDB's database when retrieving it directly using Telegraf. Since Node-RED better-supported v1.x of InfluxDB than its cloud-based (v2.0) counterpart, the older version was installed and configured. 
## Installation
### Node-RED
A pre-requisite to installing Node-RED is having git. On Windows 10, the easiest way is through installing [GitHub Desktop](https://desktop.github.com/). 
 
The best guide to installing Node-RED on Windows 10 can be found [here](https://nodered.org/docs/getting-started/windows).

**NOTE**: To run Node-RED, the command `node-red` must be run under the system directory, on Windows PowerShell with Administrator rights (Windows Key+X). 
```
PS C:\WINDOWS\system32> node-red
```
### InfluxDB
This [tutorial](https://www.qamilestone.com/post/steps-to-setup-influxdb-on-windows) provides the best guide to installing InfluxDB on Windows 10. 

**NOTE**: Step 5 in the tutorial is optional and can be skipped. 
### Grafana 
Grafana can be easily installed by following this short [guide](https://grafana.com/docs/grafana/latest/installation/windows/). 

## Setup & Usage
### InfluxDB
Per the above tutorial, InfluxDB can be run by first opening `influxd.exe`. To then start the CLI and manage your database, open `influx.exe`. InfluxDB's CLI uses a syntax that is similar to [SQL](https://www.w3schools.com/sql/). 

The basic commands include: 
- Creating a Database
```
CREATE DATABASE <DATABASE NAME>
```
- Selecting a Database 
```
USE <DATABASE NAME>
```
- Viewing your list of available databases
```
SHOW DATABASES
```
For this guide, the database `RAKAirMonitor` was created to store the sensor data. 
```
CREATE DATABASE RAKAirMonitor
```
### Node-RED
Node-RED has the advantage of intuitively visualising the management of data by representing it as a flow. The sample flow created for this guide involved retreiving data from TTN, changing it to a numeric format, and pushing it to InfluxDB. 

IMAGE

To create the flow, you must first install the palettes for TTN and InfluxDB.

IMAGE

Originally, the output from TTN for all the measurements was in a character format. eg.
```
Barometer='990hPa'
```
To make this readable on InfluxDB, the numeric part of the measurement was isolated using a function node by writing a simple script in Java.
```
msg.payload.barometer=parseFloat(msg.payload.barometer);
return msg;
``` 
Adding the debug node after the function node helps in better understanding the flow by confirming the output data matches the desired format. 

Assuming InfluxDB has been started, once the deploy button is hit, data will be pushed automatically to the chosen database at the same rate it's being sent from TTN.   
### Grafana
To be able to read information from InfluxDB, the desired database must be added as a data source on Grafana. By navigating through Grafana's UI, the necessary information can be added as shown below.

IMAGE

Finally, by selecting the correct data source, a dashboard can be created as shown below. 

IMAGE

Only prospective data will be uploaded one at a time (i.e. no historic data will be shown). Therefore, depending on your sensor's upload rate, it might take some time before you can see data points. A useful way to check when data is sent by the sensor is using the TTN Console, as highlighted below. 

IMAGE