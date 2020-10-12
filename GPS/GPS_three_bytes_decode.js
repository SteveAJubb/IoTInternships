// Set up constants for reference location

var LATITUDE_CENTER = 53.38;
var LONGITUDE_CENTER = -1.47;

function Decoder(bytes, port) {
    // Decode an uplink message from a buffer
    // {array} of bytes to an object of fields
    var decoded = {};
    // get the quadrant identifier
    var quadrant = bytes[2];

    // assign latitude and longitude variables dependent on quadrant identifier
    switch(quadrant) {
        case 1:
            decoded.latitude = Math.round((LATITUDE_CENTER + bytes[0]/(6000)) * 10000) / 10000;
            decoded.longitude = Math.round((LONGITUDE_CENTER - bytes[1]/(6000)) * 10000) / 10000;
            break;

        case 2:
            decoded.latitude = Math.round((LATITUDE_CENTER + bytes[0]/(6000)) * 10000) / 10000;
            decoded.longitude = Math.round((LONGITUDE_CENTER - bytes[1]/(6000)) * 10000) / 10000;
            break;

        case 3:
            decoded.latitude = Math.round((LATITUDE_CENTER - bytes[0]/(6000)) * 10000) / 10000;
            decoded.longitude = Math.round((LONGITUDE_CENTER - bytes[1]/(6000)) * 10000) / 10000;
            break;

        case 4:
            decoded.latitude = Math.round((LATITUDE_CENTER - bytes[0]/(6000)) * 10000) / 10000;
            decoded.longitude = Math.round((LONGITUDE_CENTER + bytes[1]/(6000)) * 10000) / 10000;
            break;
    }
    return decoded;
}
