//Import Packages
const express = require('express');

const http = require('http');
const os = require('os');
const app = express();

//Local modules
const Mqtt = require('./mqtt');
const mqtt = new Mqtt("mqtt://test.mosquitto.org");
const Influx = require('./databases/database');
const influx = Influx.Init()

//App Constants
const DATABASE_NAME = 'sensor_data';
const API_PORT = 3001;



//Connect to mqtt broker
mqtt.connect();

influx.getDatabaseNames()
  .then(names => {
    if (!names.includes(DATABASE_NAME)) {
      return influx.createDatabase(DATABASE_NAME);
    }
  })
  .then(() => {
    http.createServer(app).listen(API_PORT, function () {
      console.log('Listening on port '+API_PORT);
    })
  })
  .catch(err => {
    console.error(`Error creating Influx database!`);
    console.log(err);
  })


app.use((req, res, next) => {
  //Any code here will be run before any routes
  return next()
})

//*All below routes are largely for testing

//TEMP: Dummy test input of temperature data
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

//TEMP: See test temp data
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

//POST Requests
//TODO: Need to know format of incoming data
app.post('/input',(req,res) => {
  let data = req.body
  
  let dataPoints = []
  influx.writePoints(dataPoints)
})
