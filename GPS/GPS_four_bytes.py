from decimal import Decimal
"""
Works similarly to the three byte encoder in that it will only work if the point
is located within that GPS coordinate square of 53, -1. Note that this is a far
larger area than could be transmitted by the three byte version. The encoder
strips the gps coordinates (Ex. 53.342, -1.445 -> 0.342, 0.445) and splits them
into two bytes each. This is then sent to the decoder which will put together
the split bytes and assume that they lie within the coordinate square 53, -1.
"""

# create function that will strip the numbers
def numberStrip(number):

    return float(Decimal(number) % 1)

def encodeGPS(latitude, longitude):

    # strip the laitude and longitude coordinates and make them into 'short' types
    # short type can be up to ~65000 so need to make sure numbers are within range
    latStrip = round(abs(numberStrip(latitude))*1e5/2)
    longStrip = round(abs(numberStrip(longitude))*1e5/2)

    # create a list for the bytes to be stored in
    byteList = []

    # use bit methods to split values
    byteList.append((latStrip & 0xFF00) >> 8)
    byteList.append(latStrip & 0x00FF)
    byteList.append((longStrip & 0xFF00) >> 8)
    byteList.append(longStrip & 0x00FF)

    byteList = bytes(byteList)
    return byteList

def decodeGPS(byteList):

    # reverse the actions of the decoder
    latitude = 53 + ((byteList[0] << 8) + byteList[1])*2/1e5
    longitude = -(1 + ((byteList[2] << 8) + byteList[3])*2/1e5)

    return latitude, longitude
