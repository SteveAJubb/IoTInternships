function Decoder(bytes, port) {

    // Decode an uplink message from a buffer
    // {array} of bytes to an object of fields
    var decoded = {};
    
    // reverse the encoding bitwise operators and assume that the point lies
    // within the coordinate grid position of 53, -1
    decoded.latitude = 53 + ((bytes[0] << 8) + bytes[1])*2/1e5;
    decoded.longitude = -(1 + ((byteList[2] << 8) + byteList[3])*2/1e5);

    return decoded;
}
