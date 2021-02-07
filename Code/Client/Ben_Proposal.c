#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <SoilSensor.h>
#include <Wire.h>
#include "DHT.h"
#include "SSD1306Ascii.h"
#include "SSD1306AsciiAvrI2c.h"
///////////////////////////////////
#define SOIL_SENSOR_PIN 7
#define Broche_Echo 7 			// Broche Echo du HC-SR04 sur D7
#define Broche_Trigger 8    // Broche Trigger du HC-SR04 sur D8
#define DHTPIN 4
#define DHTTYPE DHT22
///////////////////////////////////
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(SOIL_SENSOR_PIN);
SoilSensor soilSensor(&oneWire);
SSD1306AsciiAvrI2c oled;
int profondeur_reservoir = 10; //cm

///////////////////////////////////
const char *AP_SSID = "my_ssid";
const char *AP_PWD = "ap_password";

HTTPClient http;

int delay_time_ms;
const int reference_product_number = 0xA7C789E4563F;

int server_general_portCOM = 8888;
int server_own_portCOM;
const char* SERVER_URL = "localhost://";

char SERVER_LINK[80];

struct post_commands{
  const char *first_connexion = "first_connexion";
  const char *value = "value"; //envoyer les mesures
  const char *full_value = "full_value"; //envoyer les mesures + valeur des actionneurs
};
struct server_response{
  const char *correction = "correction"; //appliquer des valeurs sur les actionneurs
  const char *value = "value"; //demande d'envoie full_value
};
struct sensor{
  const char *Temperature = "Temperature";
  const char *Humidity = "Humidity";
  const char *GroundQuality = "GroundQuality";
  const char *WaterLevel = "WaterLevel";
  const char *Luminosity = "Luminosity";
};
struct action{
  const char *Temperature = "Temperature";
  const char *Humidity = "Humidity";
  const char *WaterLevel = "WaterLevel";
  const char *Luminosity = "Luminosity";
  const char *WaterFlow = "WaterFlow";
};
struct measure{
  float Temperature;
  float Humidity;
  float GroundQuality;
  float WaterLevel;
  float Luminosity;
}

struct post_commands p;
struct server_response s;
struct sensor s;
struct action a;
struct measure m;

void setup_wifi();
int first_connection_to_server();
StaticJsonDocument<200> send_values();
float get_moisture();
byte get_i2c_address();
void display_value(char* name, float value);

void setup() {
  byte address;
  Serial.begin(9600);
  Wire.begin();
  address = get_i2c_address();
  if(address == 0){
    Serial.println("No oled screen found");
    return;
  }
  setup_wifi();

  if(first_connection_to_server() != 0){
    //ERREUR
  }
  //AFFICHER SUR L ECRAN LCD "Connection Etablie"
  soilSensor.begin();
  dht.begin();
  oled.begin(&amp;Adafruit128x64, address);
  oled.clear();
  oled.set2X();
  oled.println("Connexion établie");
  digitalWrite(Broche_Trigger, LOW); 		// On efface l'etat logique de TRIG
	delayMicroseconds(2);
	digitalWrite(Broche_Trigger, HIGH); 	// On met la broche TRIG a "1" pendant 10ÂµS
	delayMicroseconds(10);
	digitalWrite(Broche_Trigger, LOW);		// On remet la broche TRIG a "0"
}

void loop() {
  if ((WiFi.status() == WL_CONNECTED)) {
    // Not used in this example
    //Faire une mesure de tous les capteurs
    m.Temperature = dht.readTemperature();
    m.Humidity = dht.readHumidity();
    m.GroundQuality = get_moisture();
    m.WaterLevel = A COMPLETER;
    m.Luminosity = A COMPLETER;
    StaticJsonDocument<200> response = send_values();
    if(response.isNULL()){
      //ERREUR
    }
    // appliquer les corrections
    /*LUMIERE*/ = response[a.Luminosity];
    /*IRIGATION*/ = response[a.WaterFlow];
    delay_time_ms = response["sleep_duration"]; //change en fonciton jour, nuit et mode vacances
  }
  else{
    Serial.println("Connection lost...\n");
    setup_wifi();
  }
  unsigned long start_time = micros();
  if((double)(pulseIn(Broche_Echo, HIGH))*0.034/2 >= (double)profondeur_reservoir*(1-0.1)){ //si il reste 10% ou moins d'eau
    int prev_value = (double)(pulseIn(Broche_Echo, HIGH))*0.034/2;
    display_value("Remplir le réservoir jusqu'au trait", 77777777.77777777);
    while((double)(pulseIn(Broche_Echo, HIGH))*0.034/2 >= (double)profondeur_reservoir*(1-0.9)){
      delay(100); //ms
    }
    display_value("Réservoir rempli !!", 0.0);
  }
  unsigned long end_time = micros();
  while((end_time - start_time)/100 < delay_time_ms){
    m.Temperature = dht.readTemperature();
    display_value(s.Temperature, m.Temperature);
    delay(500);
    if(m.Temperature < response[a.Temperature]){
      display_value("j'ai trop froid, je veux", response[a.Temperature]);
      delay(500);
    }
    else{
      if(m.Temperature > response[a.Temperature]){
        display_value("j'ai trop chaud, je veux", response[a.Temperature]);
        delay(500);
      }
    }
    display_value(s.Humidity, m.Humidity);
    delay(500);
    display_value(s.GroundQuality, m.GroundQuality);
    delay(500);
    display_value(s.WaterLevel, m.WaterLevel);
    delay(500);
    display_value(s.Luminosity, m.Luminosity);
    delay(500);
    end_time = micros();
  }
}

StaticJsonDocument<200> send_values(){
  if (http.run() == WL_CONNECTED) {

    HTTPClient http;

    sprintf(SERVER_LINK, "%s%d/%s", SERVER_URL, server_own_portCOM, p.value);
    http.begin(SERVER_LINK);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    //on met les valeurs de chaque capteur
    doc[s.Temperature] = m.Temperature;
    doc[s.Humidity] = m.Humidity;
    doc[s.GroundQuality] = m.GroundQuality;
    doc[s.WaterLevel] = m.WaterLevel;
    doc[s.Luminosity] = m.Luminosity;

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);

    if(httpResponseCode > 0){

      String response = http.getString();
      deserializeJson(doc, response);

      //on met a jour le port de communication propre a ce systeme
      server_own_portCOM = atoi(doc["PortCOM"]);
      http.end();
      return doc;
    }
    http.end();
    StaticJsonDocument<200> err;
    err.clear();
    return ; //erreur
  }
}
int first_connection_to_server() {
  if (http.run() == WL_CONNECTED) {

    HTTPClient http;

    sprintf(SERVER_LINK, "%s%d/%s", SERVER_URL, server_general_portCOM, p.first_connexion);
    http.begin(SERVER_LINK);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    //on renseigne les capteurs presents dans ce systeme => 0 non présent ; 1 present
    doc[s.Temperature] = 1;
    doc[s.Humidity] = 1;
    doc[s.GroundQuality] = 1;
    doc[s.WaterLevel] = 1;
    doc[s.Luminosity] = 1;
    doc[a.Luminosity] = 1;
    doc[a.WaterFlow] = 1;

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);

    if(httpResponseCode > 0){

      String response = http.getString();
      deserializeJson(doc, response);

      //on met a jour le port de communication propre a ce systeme
      server_own_portCOM = atoi(doc["PortCOM"]);
      http.end();
      return 0;
    }
    http.end();
    return 1; //erreur
  }
}

float get_moisture(){
  uint16_t = moisture;
  soilSensor.wakeUp();
  soilSensor.readMoistureRaw(&moisture);
  soilSensor.sleep();
  return (float)moisture;
}

byte get_i2c_address(){
  byte error, address;
  int nDevices;

  Serial.println("Scanning...");

  nDevices = 0;
  for(address = 1; address < 127; address++ ){
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0)
    {
      Serial.print("I2C device found at address 0x");
      if (address<16)
        Serial.print("0");
      Serial.print(address,HEX);
      Serial.println("  !");

      nDevices++;
    }
    else if (error==4)
    {
      Serial.print("Unknown error at address 0x");
      if (address<16)
        Serial.print("0");
      Serial.println(address,HEX);
    }
  }
  if(nDevices == 0)
    return 0;
  else
    return address;
}

void display_value(char* name, float value){
  oled.clear();
  oled.set2X();
  oled.println(name);
  oled.set1X();
  oled.println("%f", value);
}

void setup_wifi(){
  Serial.print("Connecting to ");
  Serial.println(AP_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(AP_SSID, AP_PWD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
