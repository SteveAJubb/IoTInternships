/***
 * Original Code: https://github.com/matthijskooijman/arduino-lmic/blob/master/examples/ttn-abp/ttn-abp.ino
 * Modified by Robert Bruce
 * ***/
 
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

//OLED library and declaration for devices with OLED screens
#include <U8x8lib.h>
U8X8_SSD1306_128X64_NONAME_SW_I2C u8x8(/* clock=*/ 15, /* data=*/ 4, /* reset=*/ 16);


// This EUI must be in little-endian format, so least-significant-byte
// first. When copying an EUI from ttnctl output, this means to reverse
// the bytes. For TTN issued EUIs the last bytes should be 0xD5, 0xB3,
// 0x70.
static const u1_t PROGMEM APPEUI[8]={ 0x96, 0x2C, 0x03, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };
void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8);}

// This should also be in little endian format, see above.
static const u1_t PROGMEM DEVEUI[8]={ 0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01 };
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8);}

// This key should be in big endian format (or, since it is not really a
// number but a block of memory, endianness does not really apply). In
// practice, a key taken from ttnctl can be copied as-is.
// The key shown here is the semtech default key.
static const u1_t PROGMEM APPKEY[16] = { 0xB5, 0x69, 0x2F, 0xE4, 0x2A, 0x12, 0x9B, 0x27, 0x61, 0x3D, 0xEF, 0x1B, 0x2A, 0x5F, 0x28, 0x41 };
void os_getDevKey (u1_t* buf) {  memcpy_P(buf, APPKEY, 16);}

static osjob_t sendjob;

uint8_t mydata[] = {48,48,48}; //packet sent to TTN. Array of integers to be decoded at console
//48 is equal to '0' character in ASCII


//variables for HC-SR04 ultrasonic sensor
const int trigPin = 2;
const int echoPin = 4;
long duration;
int curr_dist;
int prev_dist = 0;


const unsigned TX_INTERVAL = 60;

// Pin mapping for Heltec LoRa 32 (V2), change as needed
const lmic_pinmap lmic_pins = {
  .nss = 18,
  .rxtx = LMIC_UNUSED_PIN,
  .rst = 14,
  .dio = {26, 35, 34}
};


//LED and Button Pins
int buttonPin = 13;
int ledPin=12;
int boardLED=25;
int lastState=0;


void onEvent (ev_t ev) {
    //LED will flash for a successful TX
    Serial.print(os_getTime());
    Serial.print(": ");
    switch(ev) {
        case EV_TXCOMPLETE:
           ledFLash(2);
           mydata[1] = 48; //reset count after TX
           Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
           u8x8.drawString(0, 2, "Data Sent");
           u8x8.drawString(0, 4, "Button Released");
           if(LMIC.dataLen) {
               // data received in rx slot after tx
               Serial.print(F("Data Received: "))
               Serial.print(LMIC.dataLen);
               Serial.print(F(" bytes for downlink: 0x"));
               for (int i = 0; i < LMIC.dataLen; i++) {
                   if (LMIC.frame[LMIC.dataBeg + i] < 0x10) {
                       Serial.print(F("0"));
                   }
                   Serial.print(LMIC.frame[LMIC.dataBeg + i], HEX);
               }
               Serial.println();
           }
           // Schedule next transmission
           os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(TX_INTERVAL), do_send);
           delay(2000);
           
          default:
            Serial.println(F("Unknown event"));
           u8x8.drawString(0, 2, "Unknown event");
            break;
    }
}

void ledFLash(int flashes){
    int lastStateLED=digitalRead(ledPin);
    for(int i=0;i<flashes;i++){
        digitalWrite(ledPin, HIGH);
        delay(300);
        digitalWrite(ledPin, LOW);
        delay(300);
    }
    digitalWrite(ledPin,lastStateLED);
}
void do_send(osjob_t* j){
    // Check if there is not a current TX/RX job running
   
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println(F("OP_TXRXPEND, not sending"));
        
    } else {
        // Prepare upstream data transmission at the next possible time.
        LMIC_setTxData2(1, mydata, sizeof(mydata)-1, 0);
        Serial.println(F("Packet queued"));
       
    }
    // Next TX is scheduled after TX_COMPLETE event.
}

void setup() {
    

    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
 
    SPI.begin(5, 19, 27);
    Serial.begin(9600);
    Serial.println(F("Starting"));

    //In/Out Pins

    pinMode(ledPin, OUTPUT);
    pinMode(buttonPin, INPUT_PULLUP);
    digitalWrite(buttonPin, HIGH);

    // LMIC init &RESET
    os_init();
    LMIC_reset();
    // Start job
    do_send(&sendjob);
}

   int count =  1;
   

void loop() {

    os_runloop_once();

    digitalWrite(trigPin, HIGH);
    delay(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    curr_dist = duration*0.034/2;   
    if (prev_dist != 0){    
        if((curr_dist > (prev_dist * 1.1))|| (curr_dist < (prev_dist * 0.9))) 
        {
            mydata [1] ++;
            
            
            do_send(&sendjob);
            delay(1000);
            Serial.print ("count: ");
            Serial.println(mydata[1]);
        }
    }
    prev_dist = curr_dist;
    
}
