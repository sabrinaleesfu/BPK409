/*
 * This code measures 25Hz data with 8G from the Sparkfun Accelerometer
 * and logs the data to a micro SD in the Sparkfun OpenLog
 * It is based on the Library for the MMA8452Q 
 * and the Library for the SparkFun Qwiic OpenLog
 * Modified by Patrick Mayerhofer July 2020
 */

/*
  Library for the MMA8452Q
  By: Jim Lindblom and Andrea DeVore
  SparkFun Electronics

  Do you like this library? Help support SparkFun. Buy a board!
  https://www.sparkfun.com/products/14587

  This sketch uses the SparkFun_MMA8452Q library to initialize
  the accelerometer and stream raw x, y, z, acceleration
  values from it.

  Hardware hookup:
  Arduino --------------- MMA8452Q Breakout
    3.3V  ---------------     3.3V
    GND   ---------------     GND
  SDA (A4) --\/330 Ohm\/--    SDA
  SCL (A5) --\/330 Ohm\/--    SCL

  The MMA8452Q is a 3.3V max sensor, so you'll need to do some
  level-shifting between the Arduino and the breakout. Series
  resistors on the SDA and SCL lines should do the trick.

  License: This code is public domain, but if you see me
  (or any other SparkFun employee) at the local, and you've
  found our code helpful, please buy us a round (Beerware
  license).

  Distributed as is; no warrenty given.
*/

#define sf 25 //change this for wanted sampling fq                    
#define tc (1000/(sf))     // time constant  
#include <Wire.h>                 // Must include Wire library for I2C
#include "SparkFun_MMA8452Q.h"    // Click here to get the library: http://librarymanager/All#SparkFun_MMA8452Q
#include "SparkFun_Qwiic_OpenLog_Arduino_Library.h"
#include "SparkFun_BMA400_Arduino_Library.h"	// http://librarymanager/All#SparkFun_BMA400

MMA8452Q accelMma8452;		// Create a new sensor object for MMA8452
BMA400 accelBma400;		// Create a new sensor object for BMA400


double x;
double y;
double z;
unsigned long last_time = 0;

OpenLog myLog; //Create instance
const byte OpenLogAddress = 42; //Default Qwiic OpenLog I2C address
char filename[] = "ACCdata.txt";


void setup() {
  Wire.begin();
  myLog.begin(); //Open connection to OpenLog (no pun intended)
  delay(500);
  myLog.append(filename);
  
	if (accelMma8452.begin() == true) {
		accelMma8452.setScale(SCALE_8G);
		accelMma8452.setDataRate(ODR_800);

		myLog.println("MMA8452Q Accelerometer is connected");		

	}
	else if(accelBma400.beginI2C(BMA400_I2C_ADDRESS_DEFAULT) == BMA400_OK){
		accelBma400.setODR(BMA400_ODR_800HZ);
		accelBma400.setRange(BMA400_RANGE_8G);

		myLog.println("BMA400 Accelerometer is connected");		
	}
	else{
		myLog.println("No Accelerometer Connected. Please check connections and read the hookup guide.");
		while (1);
	}

}

void loop() {
	if (accelMma8452.available()) {      // Wait for new data from accelerometer
		// Raw of acceleration of x, y, and z directions
		x = double(accelMma8452.getX())/256;
		y = double(accelMma8452.getY())/256;
		z = double(accelMma8452.getZ())/256;
	}
	else { // Wait for new data from accelerometer
		uint8_t powerModeBma400;		//variable for power mode value
		uint8_t *statusBma400;			//variable for status value
		statusBma400 = &powerModeBma400 +1;	//set *statusBma400 address next to address of powerModeBma400
		
		accelBma400.getMode(&powerModeBma400);	//read status at same time after modifying the library

		//To get the BMA status value, it must add code '*(power_mode+1) = reg_data;' 
		//in function 'bma400_get_power_mode' of bma400.c in library
		if(((*statusBma400) & 0x80) != 0){ //new updated data are reday
			if(accelBma400.getSensorData() == BMA400_OK){
				// Raw of acceleration of x, y, and z directions
				x = accelBma400.data.accelX;
				y = accelBma400.data.accelY;
				z = accelBma400.data.accelZ;
			}
		}
	}
		
	if (millis() >= last_time + tc) {
		last_time = millis();
		myLog.append(filename);
		myLog.print(x);
		myLog.print("\t");
		myLog.print(y);
		myLog.print("\t");
		myLog.print(z);
		myLog.print("\t");
		myLog.print(last_time);
		myLog.println();
	}
}
