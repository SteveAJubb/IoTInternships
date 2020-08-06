# Guide to connecting an ESP32 Lora Device to The Things Network

The main resources used to create this guide are:

[A TTN forum post describing the process](https://www.thethingsnetwork.org/forum/t/big-esp32-sx127x-topic-part-3/18436)

[The Arduino LoraWAN-MAC-in-C (lmic) library which contains lots of useful info](https://github.com/mcci-catena/arduino-lmic)


While this guide will contain little new information, it will hopefully make the process clearer and easier for someone else to follow. The only prerequisite for this guide will be that you have the Arduino IDE installed.


## Configuring Arduino IDE
There are two steps to configuring the IDE:

 - Adding ESP32 Devices in the board manager:
		- File  -> Preferences  -> Additional Board Manager URL’s  -> paste in: 
		 - https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
		 
 - Installing the lmic Library
		 - Sketch -> Include Library -> Library Manager -> Search “MCCI Arduino LoRaWAN Library” -> Install -> Accept 		additional libraries 

## Creating a Things Network Application


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
The last step is to configure the example sketch 




