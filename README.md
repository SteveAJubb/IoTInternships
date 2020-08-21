# Visualising Data on Grafana via Telegraf and InfluxDB Cloud

**For data from a local csv file or The Things Network**
- Retrieve Using Telegraf
- Store in a Database on InfluxDB Cloud 
- Query and Visualise onto a Dashboard Using Grafana
## InfluxDB Cloud
The cloud version of InfluxDB (v2.0) has the advantage over older versions (v1.x) of providing an interactive GUI that can make it easier for new users to monitor the contents of a given database. 
### Configuration 
- Signup for a free account on [InfluxDB Cloud](https://cloud2.influxdata.com/signup)
- Create a Bucket that will act as the database for your project
![Create-Bucket](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Create-Bucket.png)
## Installation
### Telegraf
Telegraf is an agent created by InfluxData supporting a series of configurable input plugins to suit a wide array of data sources.   

A useful guide for installing from [InfluxData](https://portal.influxdata.com/downloads/) on Windows was this short [YouTube video](https://www.youtube.com/watch?v=Vhu_UDpvBQA). 

### Grafana
Although InfluxDB Cloud has a feature to create a dashboard, Grafana was used instead, given its greater functionality. 

With a relatively simpler installation than Telegraf, the process can be easily followed with this short [guide](https://grafana.com/docs/grafana/latest/installation/windows/). 

## Setup
### Telegraf & InfluxDB Cloud
**Configuration File**

Telegraf's actions are controlled by editing the telegraf.conf file present under 
```
C:\Program Files\telegraf
```
This will act as the master configuration file for any subsequent data retrieval. Depending on the data source, a copy of the file in a local user directory will be edited and set as the default configuration file when running the agent. 

Windows Powershell with Administrator Rights (Windows Key + X) will be used as the terminal for moving the sample file and subsequently running Telegraf. 

For starters, create a folder that will act as your preferred workspace. Set this as the current directory for PowerShell by running the following command - *after replacing the directory with your own!*
```
cd 'C:\Users\Documents\IoT Project'
```
To copy the sample configuration file and paste it as 'files.conf' into the local directory, run the following command
```
telegraf -sample-config -input-filter file -output-filter influxdb > file.conf
```
**NOTE: On some occasions you might need to replace 'telegraf' from the above command with** 
```
C:\"Program Files"\telegraf\telegraf.exe  
```
Finally, open file.conf using Notepad and make sure it is saved as `UTF-8`.

**Output Plugin**

To enable Telegraf to send data to the desired bucket on InfluxDB, the output plugin is configured. By navigating through InfluxDB's UI, replace the corresponding section within the output plugin in file.conf with the automatically generated one under the 'Telegraf' tab on the left-side menu, as shown in the below figure. 

![Output-Plugin-Steps](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Output-Plugin-Steps.png)

To safeguard the security of your stored data on InfluxDB, a token acts in a similar way to a password to only enable authorised users to manipulate the database. Therefore, create an 'All Access' token as shown in the figure and use it to replace `$INFLUX_TOKEN` in file.conf within your recently copied output plugin. 

![Token-Steps](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Token-Steps.png)

For reference, the output plugin begins on line 99 in the attached configuration files. 

**Input Plugin**

This section of file.conf outlines the source and format of the data that you wish to retrieve and store into the database. 

For reference, the input plugin begins on line 607 in the attached configuration files. 

***For a csv file data source - [File Input Plugin](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/file)***

InfluxDB follows a specific [line protocol](https://v2.docs.influxdata.com/v2.0/reference/syntax/line-protocol/#:~:text=InfluxDB%20uses%20line%20protocol%20to,timestamp%20of%20a%20data%20point.&text=Lines%20separated%2), thus the csv file must be formatted accordingly. Below is a snippet of the sample csv file used as an example in this guide. 

![Excel_Format](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Excel_Format.png)

In this example, the desired data was the generation in kW. As a minimum, the measurement name, data and timestamp were defined. This meant that the first column was to be disregarded by Telegraf when retrieving the data. 

**NOTE:** 
- Store the csv file in the same folder as file.conf, otherwise include it's full directory under the 'files' variable, as exemplified below. 
```
files = ["C:\Users\Documents\IoT Project\Factory_Energy_Consumption_01032019_30032019.csv"] 
```
- Store the time-series of each variable that you wish to upload under a _seperate_ csv file.
- Per the retention policy set for the free trial of InfluxDB, the oldest allowable timestamp is _30 days_ before the current time.
- No suitable way was found for overwriting data under the same measurement name in the same bucket. Instead, the measurement name was either changed in the csv file or the data was sent to a new bucket.
- No suitable way was found for deleting individual measurements. Instead, all the bucket can be deleted. 

***For a Things Network data source - [MQTT Consumer Input Plugin](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/mqtt_consumer)***

Once a device is set up on The Things Network (TTN) and is actively sending data over LoRaWAN, the MQTT broker can be used to read the live sensor data. 

For most cases (if you are using the EU server and collecting data with a JSON format), only the following fields have to be changed from the attached reference configuration file. 

```
topics = [ "REPLACE_WITH_APPLICATION_ID/devices/+/up" ]
username = "REPLACE_WITH_APPLICATION_ID"
password = "REPLACE_WITH_ACCESS_KEY"
```
Both the Application ID and Access Key can be found in the TTN Console as shown below. 

![MQTT_Data_Steps](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/MQTT_Data_Steps.png)

### Grafana
To be able to read information from InfluxDB, the desired bucket must be added as a data source on Grafana. By navigating through Grafana's UI, the needed information such as organization name and token can be added as shown below.

![Grafana-Datasource-Steps](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Grafana-Datasource-Steps.png)

It is worth noting that the cloud version of InfluxDB (v2.0) uses Flux as a query language, whereas older versions (v1.x) use an SQL-like language known as InfluxQL. 
## Run
Once all the components within our framework are set up, the next step is to start pushing data through.
### Telegraf
After saving the configuration file, a new terminal of Windows PowerShell with Adminstrator rights should be started. 

Set the terminal's directory to the same location as the configuration file, as exemplified below. 
```
cd 'C:\Users\Documents\IoT Project'
```
To check that the correct data is being read by Telegraf, run the following command after replacing file.conf with your corresponding filename
```
C:\"Program Files"\telegraf\telegraf.exe --config ./file.conf --test
```
This following figure highlights the correct output using the sample csv data attached in this guide.

![Test-Telegraf](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Test-Telegraf.png)

Then run the following command to start pushing data.
```
C:\"Program Files"\telegraf\telegraf.exe --config ./file.conf
```
### InfluxDB Cloud
For a csv data source, you should be able to view the complete data after a few seconds on InfluxDB's Data explorer by selecting your desired bucket and setting the time range depending on your data's timestamp - (it's best to set it as past 30d and later zoom in manually).

![Data_Explorer_InfluxDB](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Data_Explorer_InfluxDB.png)

However, for live sensor data from TTN, only prospective data will be uploaded one at a time (i.e. no historic data will be shown). Therefore, depending on your sensor's upload rate, it might take some time before you can see data points. A useful way to check when data is sent by the sensor is using the TTN Console, as highlighted below. 

![Data_ttn](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Data_ttn.png)

### Grafana

For Grafana to pull the desired data from InfluxDB, a query in Flux has to be written. As illustrated below, upon selecting the desired dataset, toggling to the script editor tab will automatically generate a query in Flux which can be copied to Grafana when creating the dashboard.

![Flux_Query](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Flux_Query.png)

Within Grafana, creating a dashboard is quite straightforward. As shown, upon selecting the correct datasource created earlier, pasting the query generated from InfluxDB will quickly show the data. 

![Grafana_dashboard_steps](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Grafana_dashboard_steps.png)

**NOTE**: A common error that can stop data from showing is selecting the wrong time range in Grafana. 

More than a single variable can be added at a time to the same panel by selecting multiple measurements simultaneously on InfluxDB. Furthermore, by configuring the field option overrides, you can control features such as line colour or legend for each variable. 

![Formatting_Dashboard](https://github.com/SteveAJubb/IoTInternships/blob/Energy-Monitor-with-InfluxDBCloud/Formatting_Dashboard.png)

