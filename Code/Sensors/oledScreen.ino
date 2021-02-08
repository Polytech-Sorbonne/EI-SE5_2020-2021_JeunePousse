// Librairie pour l'afficheur OLED
// https://github.com/greiman/SSD1306Ascii

#include "SSD1306Ascii.h"
#include "SSD1306AsciiAvrI2c.h"
 
#define I2C_ADDRESS 0x3C // utiliser le code scanner i2c pour trouvr l'adresse de l'écran
 
SSD1306AsciiAvrI2c oled;
 
void setup() {
 
  oled.begin(&amp;Adafruit128x64, I2C_ADDRESS);
  oled.setFont(Adafruit5x7);  
  oled.clear();
  oled.set2X();
  oled.println("Test ");
  oled.set1X();
  oled.println("test ecran oled");
  oled.println("JEUNE POUSSE");
 
}
void loop() {
 
}