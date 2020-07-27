/**
 * File that controls connecting to the database
 * @author Nathan Brown, Harrison Fretwell
 */
const Influx = require('influx')

module.exports = class Database{
    
    /**
     * Connect to influxdb and return instance of influxdb
     */
    static Init(){
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
        return influx;
    }
}

