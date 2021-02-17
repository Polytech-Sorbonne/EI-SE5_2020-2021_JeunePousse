/* Inspiré de https://create.arduino.cc/projecthub/hubmartin/soil-sensor-with-arduino-esp8266-esp32-2bc942
 * VOIR RESISTANTCE EN PULL UP DE 4.7 kOhms A LA PIN VCC
 A REGARDER, LIEN D'APOLLINE : https://wiki.dfrobot.com/Waterproof_Capacitive_Soil_Moisture_Sensor_SKU_SEN0308#target_3

Soil Moisture Sensor
====================

Arduino Library for HARDWARIO Soil Sensor
Author: podija https://github.com/podija
        hubmartin https://github.com/hubmartin

HARDWARIO is a digital maker kit developed by https://www.hardwario.com/

Product: https://shop.hardwario.com/soil-sensor/
Specs: https://developers.bigclown.com/hardware/about-soil-moisture-sensor
Firmware: https://developers.bigclown.com/firmware/how-to-soil-moisture-sensor
Forum: https://forum.bigclown.com/

MIT License

This example uses HARDWARIO Soil Sensor for soil moisture and temperature measurement. Measured data are printed on serial port in text format. 

*/
#include <OneWire.h>
#include <SoilSensor.h>

// Add a 4k7 pull-up resistor to this pin
#define SOIL_SENSOR_PIN 7

OneWire oneWire(SOIL_SENSOR_PIN);
SoilSensor soilSensor(&oneWire);

void setup() 
{
  Serial.begin(115200);
  Serial.println("Début Soil Sensor");
  
  soilSensor.begin();
}

void loop()
{
  soilSensor.wakeUp();
  
  float temperature;
  soilSensor.readTemperatureCelsius(&temperature);
  Serial.print("Temperature:  ");
  Serial.print(temperature);
  Serial.println("°C");

  uint16_t moisture;
  soilSensor.readMoistureRaw(&moisture);
  Serial.print("Moisissure:  ");
  Serial.print(moisture);
  Serial.println();
   
  soilSensor.sleep();
  delay(2000); 
}
