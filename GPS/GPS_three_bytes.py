"""
    This application assumes that both the encoder and decoder know of some
    arbritrary center point. The distance between the GPS coordinates of the device
    being tracked from the center point is transmitted. This shortens the message
    as only 3 bytes need to be sent, the absolute latitude difference,
    absolute longitude difference, and an identifier to specify the signs of the
    transmitted differences.
"""

"""NOTE
    if a point is inputted that is too far away from the center point
    the application will fail as the difference in latitude and longitude will
    be too large to put into a byte without losing too much information
    ex. Centering in Sheffield will fail just past Rotherham
"""



# arbritrary geographical center
# using Sheffield central for this application
LATITUDE_CENTER = 53.38
LONGITUDE_CENTER = -1.47

# uses cartesian coordinates as input
# based on the sign of each it will return the quadrant a point is located
def getQuadrant(y,x):

    if (y >= 0 and x >= 0):

        return 1

    elif (y >= 0 and x <= 0):

        return 2

    elif (y <= 0 and x <= 0):

        return 3

    elif (y <= 0 and x >= 0):

        return 4

# takes latitude and longitude positional coordinates as input
# converts them into unsigned bytes storing the distance between the point and the center
# additionally returns the quadrant that the point is in (sign identifier)
# allowing decoder to know where to put a negative sign
def encodeGPS(lat,long):

    # find distance between the point and the center
    # convert to unsigned bytes
    latDiff = round((lat-LATITUDE_CENTER)*(6000))
    longDiff = round((long-LONGITUDE_CENTER)*(6000))

    # from signs of distances find quadrant
    quadrant = getQuadrant(latDiff, longDiff)

    # create and return a list of bytes
    # [latitude difference, longitude difference, quadrant]
    byteList = bytes([abs(latDiff),abs(longDiff),quadrant])
    return byteList

# takes list of bytes [latDiff, longDiff, quadrant]
# uses center point and latitude and longitude distances from itself
# returns latitude and longitude coordinates of the point as list
def decodeGPS(GPSBytes):

    quadrantDecoded = GPSBytes[2]

    if (quadrantDecoded == 1):

        latDecoded = round((LATITUDE_CENTER + GPSBytes[0]/(6000)),5)
        longDecoded = round((LONGITUDE_CENTER + GPSBytes[1]/(6000)),5)

    elif (quadrantDecoded == 2):

        latDecoded = round((LATITUDE_CENTER + GPSBytes[0]/(6000)),5)
        longDecoded = round((LONGITUDE_CENTER - GPSBytes[1]/(6000)),5)

    elif (quadrantDecoded == 3):

        latDecoded = round((LATITUDE_CENTER - GPSBytes[0]/(6000)),5)
        longDecoded = round((LONGITUDE_CENTER - GPSBytes[1]/(6000)),5)

    elif (quadrantDecoded == 4):

        latDecoded = round((LATITUDE_CENTER - GPSBytes[0]/(6000)),5)
        longDecoded = round((LONGITUDE_CENTER + GPSBytes[1]/(6000)),5)

    return latDecoded,longDecoded
