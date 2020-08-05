// Set up constants for reference location

const LATITUDE_CENTER = 53.380904;
const LONGITUDE_CENTER = -1.470084;

function Decoder(bytes, port) {
    // Decode an uplink message from a buffer
    // {array} of bytes to an object of fields
    var decoded = {};
    // get the quadrant identifier
    var quadrant = bytes[2];

    // assign latitude and longitude variables dependent on quadrant identifier
    switch(quadrant) {
        case 1:
            decoded.latitude = round(((bytes[0]/(750000/256) + LATITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            decoded.longitude = round(((bytes[1]/(750000/256) + LONGITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            break;

        case 2:
            decoded.latitude = round(((bytes[0]/(750000/256) + LATITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            decoded.longitude = round(((bytes[1]/(750000/256) - LONGITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            break;

        case 3:
            decoded.latitude = round(((bytes[0]/(750000/256) - LATITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            decoded.longitude = round(((bytes[1]/(750000/256) - LONGITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            break;

        case 4:
            decoded.latitude = round(((bytes[0]/(750000/256) - LATITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            decoded.longitude = round(((bytes[1]/(750000/256) + LONGITUDE_CENTER) + Number.EPSILON) * 10000) / 10000;
            break;
    }
    return decoded;
}
