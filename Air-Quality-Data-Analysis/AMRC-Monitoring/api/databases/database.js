/**
 * File that controls connecting to the database
 * @author Nathan Brown, Harrison Fretwell
 */
const Influx = require('influx')

module.exports = class Database{
    
    /**
     * Connect to influxdb and return instance of influxdb
     */
    static Init(dbName){
        const influx = new Influx.InfluxDB({
            host: 'localhost',
            database: dbName,
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

