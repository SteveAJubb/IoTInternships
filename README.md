# Using InfluxDB and Grafana to Display Geographical Data

## Installation

### InfluxDB

Simple to install. I used https://websiteforstudents.com/how-to-install-influxdb-on-ubuntu-18-04-16-04/ as a guide on how to install it on Ubuntu. This seemed to work well and tells you how to configure InfluxDB so that you can send queries to it using http.

### Grafana

Grafana is a bit trickier to install than InfluxDB however when following the right guide it is not too tedious. Grafana provides a relatively
simple guide here https://grafana.com/docs/grafana/latest/installation/debian/. However, at the time of writing, one plugin that I'm using is
not supported in the latest edition of Grafana. Therefore, you will need to install the right .deb package. I got things working well in Grafana 7.0.6 but hopefully the plugins will be updated soon so you can just grab the latest version. To install a specific version please visit this webpage https://grafana.com/grafana/download and select the version of your choice.

#### Additional Grafana Plugin Installation

* WorldMap Panel: https://grafana.com/grafana/plugins/grafana-worldmap-panel
* TrackMap Panel: https://grafana.com/grafana/plugins/alexandra-trackmap-panel

## Usage

### InfluxDB

To access the InfluxDB server from the command line use:

```

$ influx

```
It uses similar syntax to SQL. Ex:

```

$ CREATE DATABASE <DATABASE NAME>
$ USE <DATABASE NAME>

```

One important thing to note is that data of a similar type is accessed through the a measurement (specified when inputting the infomation to InfluxDB in whatever way). Measurements usually contain data fields (<field>) and classification tags (<tag>). Ex:

```

$ SELECT <field> FROM <measurement> WHERE <tag>

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

### Grafana

I would recommend using this https://grafana.com/docs/grafana/latest/getting-started/getting-started/ from the official Grafana documentation to get yourself started. I found that playing around with things is the best way to start.

### Grafana WorldMap Plugin

Documentation for the WorldMap Panel plugin in can be found at this website https://grafana.com/grafana/plugins/grafana-worldmap-panel. For my purposes, I only ever used the table query method. Here you can also find how to install the plugin correctly. For this to work, objects need to be passed to InfluxDB with two tags (one for latitude and longitude), and a field with some kind of metric value. For my purposes this was the NO2 levels in the air. NOTE: It is EXTREMELY important that you use an ALIAS in your query to influx. This ALIAS should tell Grafana to select your data AS METRIC. This METRIC label is what the WorldMap panel sees when displaying your data on the map.

A typical JSON input into InfluxDB might look something like this:

```

   {
        "measurement": "air.quality",
        "tags": {
            "latitude": 53.3834567
            "longitude": -1.4589922
        },
        "fields": {
            "NO2_ppb": 14
        }
    }

```

### Grafana Trackmap Plugin

Information and installation guides may be found here https://grafana.com/grafana/plugins/alexandra-trackmap-panel. Note that there is another panel by the same name but with less features. To use this panel there needs to be objects that contain two fields, one for longitude, and one for latitude. It took me a while to get the Grafana query right for this plugin but I found this one to work a charm: 

```
SELECT "time" AS "time_index", "latitude" AS "lat", "longitude" AS "lon" FROM "location" WHERE $timeFilter GROUP BY time_index fill(null)

```

From the settings menu you can display that data as a heatmap, antpath, or hexbin.

A typical JSON input into InfluxDB might look something like this:

```

    {
        "measurement": "location",
        "fields": {
            "latitude": 53.5234363,
            "longitude": -1.4324670
        }
    }

```



