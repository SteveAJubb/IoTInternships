//Import Packages
const express = require('express');
const bodyParser = require('body-parser')
const http = require('http');
const os = require('os');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

//Local modules
const Mqtt = require('./mqtt');
const mqtt = new Mqtt("mqtt://test.mosquitto.org");
const Influx = require('./databases/database');

//App Constants
const DATABASE_NAME = 'sensor_data';
const API_PORT = 3001;

const influx = Influx.Init(DATABASE_NAME)


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

app.post('/ttn',(req,res) => {
  console.log(req.body)
})

let oldTemp = 0
let temperature = Math.random()*100;
//TEMP: Dummy test input of temperature data
app.get('/test-input', (req,res)=> {
    let timeout = setInterval(() => {
      oldTemp = temperature 
      writeTemp = oldTemp + (Math.random() - 0.5);
      influx.writePoints([{
          measurement: 'Temperature',
          tags:{device: 1},
          fields: {writeTemp}
      }])
  },500)
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