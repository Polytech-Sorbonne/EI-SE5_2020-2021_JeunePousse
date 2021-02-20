#include <analogWrite.h>

void setup()
{
  Serial.begin(115200); // open serial port, set the baud rate to 9600 bps
}
void loop()
{
  Serial.println(analogRead(34)); //connect sensor and print the value to serial
      
  delay(100);
}
