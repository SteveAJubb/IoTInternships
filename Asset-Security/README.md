# Guide to connecting an ESP32 Lora Device to The Things Network

The main resources used to create this guide are:

[A TTN forum post describing the process](https://www.thethingsnetwork.org/forum/t/big-esp32-sx127x-topic-part-3/18436)

[The Arduino LoraWAN-MAC-in-C (lmic) library which contains lots of useful info](https://github.com/mcci-catena/arduino-lmic)


While this guide will contain little new information, it will hopefully make the process clearer and easier for someone else to follow. The only prerequisite for this guide will be that you have the Arduino IDE installed.


## Configuring Arduino IDE
There are two steps to configuring the IDE:

 - Adding ESP32 Devices in the board manager:
		 File  -> Preferences  -> Additional Board Manager URL’s  -> paste in: 
		  https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
		 
 - Installing the lmic Library
		 Sketch -> Include Library -> Library Manager -> Search “MCCI Arduino LoRaWAN Library” -> Install
		  ->  Accept 		additional libraries 

## Creating a Things Network Application
To create a things network Application first go to [The TTN Website](https://console.thethingsnetwork.org/)

Create and account and then add an application. Neither the Application ID or Description matter just put whatever is useful. Leave the Handler Registration as default. 

Then under Devices click register device.  Again the Device ID does not matter. Click the button to auto generate the Device EUI and then click register. This device overview page will be used later to add the device info to our Arduino Code.


## Configuring the Library
There is a configuration file within the library once it is installed. As this library works in various regions and with multiple transceiver types we need to tell it what we are using. 
To do this open the lmic_project_config text file. This is located inside the lmic library you just installed the default location is something like:

    Documents\Arduino\libraries\MCCI_LoRaWAN_LMIC_library\project_config

Options are selected by un-commenting the settings that you want so for our purposes your text file should look like this:

    // project-specific definitions 
    #define CFG_eu868 1
    //#define CFG_us915 1
    //#define CFG_au915 1
    //#define CFG_as923 1
    // #define LMIC_COUNTRY_CODE LMIC_COUNTRY_CODE_JP	/* for as923-JP */
	//#define CFG_kr920 1
	//#define CFG_in866 1
	#define CFG_sx1276_radio 1
	//#define LMIC_USE_INTERRUPTS



## Configuring the Device
The last step is to configure the example sketch. This step will be different depending on the device used. For this example a ESP32 LoRa Device is used. Below is a picture of what you will see on the TTN console. The format of the EUI's is important and can be changed using the buttons highlighted.
Normally this information should not be shared, however this is device is only used for example. 

![Image of TTN Info](https://github.com/SteveAJubb/IoTInternships/blob/Asset-Security/LoraWan%20and%20TTN/Guide%20Pictures/Device_Overview.png)
    
    // This EUI must be in little-endian format, so least-significant-byte
    // first. When copying an EUI from ttnctl output, this means to reverse
    // the bytes. For TTN issued EUIs the last bytes should be 0xD5, 0xB3,
    // 0x70.
    static const u1_t PROGMEM APPEUI[8]={ 0xBD, 0x2E, 0x03, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };
    void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8);}
    / This should also be in little endian format, see above.
    static const u1_t PROGMEM DEVEUI[8]={ 0xE0, 0x35, 0x8A, 0xDB, 0xA1, 0xC7, 0xC7, 0x00 };
    void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8);}
    // This key should be in big endian format (or, since it is not really 
    // number but a block of memory, endianness does not really apply). In
    // practice, a key taken from ttnctl can be copied as-is.
    static const u1_t PROGMEM APPKEY[16] = { 0x08, 0x80, 0x4B, 0xEC, 0x6E, 0x31, 0xD0, 0xA4, 0xD2, 0x6F, 0x6C, 0x68, 0xDD, 0x98, 0xA4, 0x7B };
    void os_getDevKey (u1_t* buf) {  memcpy_P(buf, APPKEY, 16);}

The next and final step is to change the pin mapping used in the code. This is to tell the code which pins are used to control the tranciever. For the ESP32 in our example you can simply delete the exisiting pin mapping and paste in the code below. For other devices you will need to find the relevant pins.

    
    // Pin mapping
    const lmic_pinmap lmic_pins = {
    .nss = 18,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = LMIC_UNUSED_PIN, // was "14,"
    .dio = {26, 33, 32},
    };


## Sending Hello World!

The code can now be uploaded to your ESP32 device. The Serial monitor can be used to see the current status. A successful joining the network should look similar to the image below.

![Image of Serial Output](https://github.com/SteveAJubb/IoTInternships/blob/Asset-Security/LoraWan%20and%20TTN/Guide%20Pictures/Serial_Output.png)
