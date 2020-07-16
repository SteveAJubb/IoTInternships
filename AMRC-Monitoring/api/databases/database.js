/**
 * File that controls connecting to the database
 * @author Nathan Brown, Harrison Fretwell
 */

/**
 * Mongoose module
 * @constant
 */
const mongoose = require('mongoose');

/**
 * ObjectId from mongo modle
 * @constant
 */
const ObjectId = require('mongodb').ObjectID;

//The URL which will be queried. Run "mongod.exe" for this to connect

mongoose.Promise = global.Promise;

/**
 * Set for local host port
 * @constant
 */
const mongoDB = 'mongodb://localhost:27017/pitch-inIOT';

//Connect to the database
mongoose.Promise = global.Promise;
try {
    connection = mongoose.connect(mongoDB, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        checkServerIdentity: false,
    });
    console.log('connection to mongodb worked!');

} catch (e) {
    console.log('error in db connection: ' + e.message);
}

