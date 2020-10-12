float LATITUDE_CENTER = 53.3809;
float LONGITUDE_CENTER = -1.4701;

int getQuadrant(float y, float x) {

  if (y >= 0 and x >= 0) {

    return 1;
  }

  else if (y >= 0 and x <= 0){

    return 2;
  }

  else if (y <= 0 and x <= 0) {

    return 3;
  }

  else if (y <= 0 and x >= 0) {

    return 4;
  }

}

void GPSEncode(lat, long){

  int latDiff = round((lat-LATITUDE_CENTER)*(750000/256));
  int longDiff = round((long-LONGITUDE_CENTER)*(750000/256));

  int quadrant = getQuadrant(latDiff,longDiff);

  byte GPSBytes[3] = {byte(latDiff), byte(longDiff), byte(quadrant)};

  //send bytes over ttn
}

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  // get position of bike from sensor
  // can't code yet as don't have sensor


}
