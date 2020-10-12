import math
from influxdb import InfluxDBClient
from geopy.distance import geodesic
from datetime import datetime, timedelta

# set up the influxdb client and connect to the trackmap database
client = InfluxDBClient(host='127.0.0.1', port=8086, username='', password='', database='')

# query the last piece of data stored under the 'carTrack' measurement
# however this script can be used to manage multiple messages
routeData = client.query("<QUERY>") #Ex. SELECT ... FROM ... WHERE ...

# set the time format to be used by the python datetime module
# this corresponds to how influx stores time data
time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
# creates a generator object that parses the point gathered
influxPoints = routeData.get_points()

# create a more accessible list of points from the generator object
def pointsFromInflux(influxPoints):

    # create empty list of coordinate get_points and relevant properties
    points = []
    # transfer data from the generator object 'points' into useable list coords
    for influxPoint in influxPoints:
        # time is transferred to a datatime object
        influxPoint['time'] = datetime.strptime(influxPoint['time'], time_format)
        points.append(influxPoint)

    return points

# function to calculate position change in meters from two pairs of latitude
# and longitude coordinates (optional altitude data as well)
def positionChange(coordinate1, coordinate2):

    # calculate the distance travelled in the x-y plane using geopy
    # geopy takes two tuples for latitude and longitude and outputs a distance
    groundDist = geodesic((coordinate2['latitude'],coordinate2['longitude']),(coordinate1['latitude'],coordinate1['longitude'])).m # in meters

    # check if both coordinates have a corresponding altitude
    if coordinate1['altitude'] and coordinate2['altitude']:

        # calculate the distance travelled in the z plane
        altDist = coordinate2['altitude'] - coordinate1['altitude']
        # calculate the overall distance travelled
        dist = math.sqrt(groundDist**2 + altDist**2)

    else:

        dist = groundDist

    return dist

# function that takes a list of position objects {'latitude':..., 'longitude'... etc}
# and the number of points needing to be returned (in reverse chronological order)
# returns a list of speedPoint objects (same as positionPoint but with speed, distance, time elapsed)
def movementList(positionPoints, number=None):

    # if no number of points specified, grab them all
        number = len(positionPoints)-1
        if not number:

    # create empty list speedPoints to store original data and calculated data
    speedPoints = []

    # loop through points list and append to speedPoints with additional calculated data
    for i in range(0, number):
        # get analyse data and calculate speed
        # calculate time difference between most recent point and one prior
        timeDiff = positionPoints[-(i+1)]['time'] - positionPoints[-(i+2)]['time']
        # avoid math errors
        if timeDiff.seconds > 0:

            # calculate distance using positionChange function
            distance = positionChange(positionPoints[-(i+2)],positionPoints[-(i+1)])
            # calculate the speed
            speed = distance/timeDiff.seconds
            # append it all to speedpoints
            speedPoints.append({'latitude': positionPoints[-(i+1)]['latitude'], 'longitude': positionPoints[-(i+1)]['longitude'], 'time': positionPoints[-(i+1)]['time'], 'timeDiff': timeDiff.seconds, 'positionChange': distance, 'speed': speed})
    return speedPoints

# create a function to write points to influxdb
def writePoints(speedDataSet):

    # create empty list of data to be filled with JSON objects
    data = []

    # add the points under the measurement speeds
    for speedData in speedDataSet:

        data.append(
        {
            "measurement": 'speeds',
            "tags": {
                "latitude": speedData['latitude'],
                "longitude": speedData['longitude']
            },
            "fields": {
                "speed": int(speedData['speed']),
                "timeDiff": speedData['timeDiff']
            },
            "time": f"{speedData['time']:%Y-%m-%dT%H:%M:%S.%fZ}"
        })
    # write the points to a database
    client.write_points(data, database='trackmap', time_precision='s', batch_size=10000, protocol='json')


# every time this file is called, it will calculate the most recent speed
# and write it to a speeds database
# this can be changed to suit your purpose
writePoints(movementList(pointsFromInflux(influxPoints),1))
