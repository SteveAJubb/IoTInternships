// Set up constants for reference location

var LATITUDE_CENTER = 53.380904;
var LONGITUDE_CENTER = -1.470084;

function Decoder(bytes, port) {
    // Decode an uplink message from a buffer
    // {array} of bytes to an object of fields
    var decoded = {};
    // get the quadrant identifier
    var quadrant = bytes[2];

    // assign latitude and longitude variables dependent on quadrant identifier
    switch(quadrant) {
        case 1:
            decoded.latitude = Math.round(((bytes[0]/(750000/256) + LATITUDE_CENTER)) * 10000) / 10000;
            decoded.longitude = Math.round(((bytes[1]/(750000/256) + LONGITUDE_CENTER)) * 10000) / 10000;
            break;

        case 2:
            decoded.latitude = Math.round(((bytes[0]/(750000/256) + LATITUDE_CENTER)) * 10000) / 10000;
            decoded.longitude = Math.round(((bytes[1]/(750000/256) - LONGITUDE_CENTER)) * 10000) / 10000;
            break;

        case 3:
            decoded.latitude = Math.round(((bytes[0]/(750000/256) - LATITUDE_CENTER)) * 10000) / 10000;
            decoded.longitude = Math.round(((bytes[1]/(750000/256) - LONGITUDE_CENTER)) * 10000) / 10000;
            break;

        case 4:
            decoded.latitude = Math.round(((bytes[0]/(750000/256) - LATITUDE_CENTER)) * 10000) / 10000;
            decoded.longitude = Math.round(((bytes[1]/(750000/256) + LONGITUDE_CENTER)) * 10000) / 10000;
            break;
    }
    return decoded;
}
