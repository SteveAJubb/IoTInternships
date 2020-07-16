//Import Packages
const express = require('express');
const Mqtt = require('./mqtt');
const Influx = require('influx')
const MqttClient = new Mqtt("mqtt://test.mosquitto.org");
const http = require('http');
const os = require('os');
const app = express();


//Connect to mqtt broker
MqttClient.connect();

//Connec to local influx database
const influx = new Influx.InfluxDB({
    host: 'localhost',
    database: 'express_response_db',
    schema: [
      {
        measurement: 'response_times',
        fields: {
          path: Influx.FieldType.STRING,
          duration: Influx.FieldType.INTEGER
        },
        tags: [
          'host'
        ]
      }
    ]
  })

influx.getDatabaseNames()
  .then(names => {
    if (!names.includes('express_response_db')) {
      return influx.createDatabase('express_response_db');
    }
  })
  .then(() => {
    http.createServer(app).listen(3001, function () {
      console.log('Listening on port 3001')
    })
  })
  .catch(err => {
    console.error(`Error creating Influx database!`);
    console.log(err);
  })



//Routes for backend
app.use((req, res, next) => {
  //Any code here will be run before any routes
  return next()
})

//*All below routes are largely for testing

//Dummy test input of temperature data
app.get('/test-input', (req,res)=> {
    let timeout = setInterval(() => {
      let temperature = Math.random()*100;
      influx.writePoints([{
          measurement: 'Temperature',
          tags:{device: 1},
          fields: {temperature}
      }])
  },50)
})

//See test temp data
app.get('/temps', function (req, res) {
  influx.query(`
    select * from Temperature
    order by time desc
  `).then(result => {
    res.json(result)
  }).catch(err => {
    res.status(500).send(err.stack)
  })
})
