// Ahmed Haroun

// This script is written for the ESP 8266 D1 mini standalone board
// Not compatible with the Arduino UNO
// The script connects the board to an MQTT server to publish
// the BME 280 sensortemperature data

// ESP, MQTT and BME libraries must be installed using the library manager
 #include <ESP8266WiFi.h>
 #include <PubSubClient.h>
 #include <Wire.h>
 #include <Adafruit_Sensor.h>
 #include <Adafruit_BME280.h>

 Adafruit_BME280 bme;
 
 // Update these with your Network info (do not use corporate networks with tons of security)
 const char* ssid =         "";
 const char* password =     "";
 const char* mqtt_server =  "test.mqtt.org";   // A private MQTT network can be used
 
// Setup the Publish and Subscribe Client 
 WiFiClient espClient; //name
 PubSubClient client(espClient);
 long lastMsg = 0;
 char msg[50];
 int value = 0;

 void setup() {
   pinMode(2, OUTPUT);                  // Initialize the BUILTIN_LED pin as an output
   Serial.begin(115200);
   bme.begin(0x76);                     // I2C adress
   setup_wifi();
   client.setServer(mqtt_server, 1883); // Port set to 1883 by default
   client.setCallback(callback);
 }

 void setup_wifi() {

   delay(10);
   // We start by connecting to a WiFi network
   Serial.println();
   Serial.print("Connecting to ");
   Serial.println(ssid);

   WiFi.begin(ssid, password);

// Display success message when WIFI connects
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");                // Time taken to connect
   }

   Serial.println("");
   Serial.println("WiFi connected successfully"); 
   Serial.println("IP address: ");
   Serial.println(WiFi.localIP());
 }

 void callback(char* topic, byte* payload, unsigned int length) {
   Serial.print("Message arrived [");
   Serial.print(topic);
   Serial.print("] ");
   for (int i = 0; i < length; i++) {
     Serial.print((char)payload[i]);
   }
   Serial.println();

   // Switch on the LED if an 1 was received as first character
   if ((char)payload[0] == '0') {
      Serial.println("LOW");
     digitalWrite(2, LOW);   // Turn the LED on (Note that LOW is the voltage level
     // but actually the LED is on; this is because
     // it is acive low on the ESP-01)
   } 

  if ((char)payload[0] == '1') {
     Serial.println("HIGH");
     digitalWrite(2, HIGH);  // Turn the LED off by making the voltage HIGH
   }

 }

 void reconnect() {
   // Loop until we're reconnected
   while (!client.connected()) {
     Serial.print("Attempting MQTT connection...");
     // Attempt to connect
     if (client.connect("ESP8266Client")) {
       Serial.println("connected");
       // Once connected, publish an announcement...
       client.publish("home/livingroom/temperature", "Hello World");
       // and resubscribe
       client.subscribe("home/livingroom/temperature");
     } else {
       Serial.print("failed, rc=");
       Serial.print(client.state());
       Serial.println(" try again in 5 seconds");
       // Wait 5 seconds before retrying
       delay(5000);
     }
   }
 }
 void loop() {

   if (!client.connected()) {
     reconnect();
   }
   client.loop();

// bme sensor value must be converted into a string to publish on MQTT
   long now = millis();
   if (now - lastMsg > 2000) {  
     lastMsg = now;
     ++value;
     snprintf (msg, 75, "%f", bme.readTemperature());  // message string format to include sensor data
     Serial.print("Publish message: ");
     Serial.println(msg);
     
     client.publish("home/livingroom/temperature",msg);
   }
   client.disconnect();  // disconnect from MQTT broker
  delay(1000);          // print new values every 1 Minute
 }
