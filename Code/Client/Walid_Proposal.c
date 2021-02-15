#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "Adafruit_VEML7700.h"  //Capteur luminosité
#include <OneWire.h>
#include <SoilSensor.h>
#include <Wire.h>               //Ecran
#include <Adafruit_GFX.h>       //Ecran
#include <Adafruit_SSD1306.h>   //Ecran
#include "DHT.h"                //Capteur temperature
#include "SSD1306Ascii.h"
#include "SSD1306AsciiAvrI2c.h"
///////////////////////////////////
#define SOIL_SENSOR_PIN 7   //Add a 4k7 pull-up resistor to this pin
#define Broche_Echo 25 			// Broche Echo du HC-SR04 sur D25
#define Broche_Trigger 33   // Broche Trigger du HC-SR04 sur D33
#define DHTPIN 4
#define DHTTYPE DHT22

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
///////////////////////////////////
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(SOIL_SENSOR_PIN);
SoilSensor soilSensor(&oneWire);
SSD1306AsciiAvrI2c oled;
int profondeur_reservoir = 10; //cm
Adafruit_VEML7700 veml = Adafruit_VEML7700(); //Luminosité
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1); // Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
//Capteur distance
int MesureMaxi = 300;       // Distance max
int MesureMini = 3;       // Distance min
long Duree;
long Distance;

volatile double waterFlow;
const int PINPOMPE = 12;
const int PINLED = 13;
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
};

struct post_commands post;
struct server_response server_rep;
struct sensor sensor;
struct action action;
struct measure mesure;

void setup_wifi();
StaticJsonDocument<200> send_values();
int first_connection_to_server();
void latence();
void alimentation(char *a, char *b);
void water();
void water_ecran(int a);
void temperature_ecran(int a);
void humidity_ecran(int a);
float get_moisture_soil();
float get_temperature_soil();
float get_temperature();
float get_debit(); // en Litre
float get_humidity();
float get_distance();
float get_luminosity();
byte get_i2c_address(); //Pas utile selon moi
void ecran(char* name, float value);
void setup_wifi();



void setup()
{
  byte address;
  Serial.begin(115200);
  //setup pompe et panneau LED
  pinMode(PINPOMPE, OUTPUT);
  pinMode(PINLED, OUTPUT);
  //setup luminosité
  while(!Serial)
  {
    delay(10);
  }
  Serial.begin(115200);
  Serial.println("Adafruit VEML7700 Test");
  if (!veml.begin())
  {
    Serial.println("Sensor luminosity not found");
    while (1);
  }
  Serial.println("Sensor luminosity found");
     
  veml.setGain(VEML7700_GAIN_1);
  veml.setIntegrationTime(VEML7700_IT_800MS);
  Serial.print(F("Gain: "));
  switch (veml.getGain())
  {
    case VEML7700_GAIN_1: Serial.println("1"); break;
    case VEML7700_GAIN_2: Serial.println("2"); break;
    case VEML7700_GAIN_1_4: Serial.println("1/4"); break;
    case VEML7700_GAIN_1_8: Serial.println("1/8"); break;
  }
  Serial.print(F("Integration Time (ms): "));
  switch (veml.getIntegrationTime())
  {
    case VEML7700_IT_25MS: Serial.println("25"); break;
    case VEML7700_IT_50MS: Serial.println("50"); break;
    case VEML7700_IT_100MS: Serial.println("100"); break;
    case VEML7700_IT_200MS: Serial.println("200"); break;
    case VEML7700_IT_400MS: Serial.println("400"); break;
    case VEML7700_IT_800MS: Serial.println("800"); break;
  }
  //veml.powerSaveEnable(true);
  //veml.setPowerSaveMode(VEML7700_POWERSAVE_MODE4);
  veml.setLowThreshold(10000);
  veml.setHighThreshold(20000);
  veml.interruptEnable(true);
  //setup Distance
  pinMode(Broche_Trigger, OUTPUT);  // Broche Trigger en sortie
  pinMode(Broche_Echo, INPUT);    // Broche Echo en entree
  //setup Ecran
  Wire.begin();
  //setup WiFi
  setup_wifi();
  //setup sol
  soilSensor.begin();
  //setup Temperature et Humidity
  dht.begin();
  //setup Débit d'eau
  waterFlow = 0;
  attachInterrupt(0, pulse, RISING);  //DIGITAL Pin 2: Interrupt 0
  //setup all
  if(first_connection_to_server() != 0)
  {
    //ERREUR
  }
}

void loop()
{
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

StaticJsonDocument<200> send_values()
{
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

int first_connection_to_server()
{
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

void latence()
{
  delay(30 * 60 * 1000); // wait for 30 minutes
}

void alimentation(char *a, char *b)
{
  if(b="ouvert")
  {
    if(a="pompe")
    {
      digitalWrite(PINPOMPE, HIGH);
    }
    else//panneau LED
    {
      digitalWrite(PINLED, HIGH);
    }
  }
  else //ferme
  {
    if (a="pompe")
    {
      digitalWrite(PINPOMPE, LOW);
    }
    else //panneau LED
    {
      digitalWrite(PINLED, LOW);
    }
  }
}

void water()
{
  while(get_debit()!=1)
  {
    alimentation("pompe", "ouvert");
  }
  alimentation("pompe", "ferme")
  ecran("Arrosage de la plante terminée",0);
}

void light() //IL FAUDRAIT QUE CETTE FONCTION NE SOIT PAS APPELER POUR UNE CERTAINE PERIODE DE TEMPS ET FAUT L'ETEINDRE
{
  if(get_luminosity() < SEUIL_LUMINOSITY)
  {
    alimentation("panneauLED", "ouvert");
  }
}

void water_ecran(int a)
{
  if(a==-1)
  {
    ecran("Réservoir niveau d'eau TRES faible",0)
  }
  else if(a=1)
  {
    ecran("Réservoir niveau d'eau optimale",0)
  }
  else
  {
    ecran("Réservoir niveau d'eau faible",0)
  }
}

void temperature_ecran(int a)
{
  if(a==-1)
  {
    ecran("La plante a froid",0)
  }
  else if(a=1)
  {
    ecran("La plante a chaud",0)
  }
  else
  {
    ecran("Température de la plante optimale",0)
  }
}

void humidity_ecran(int a)
{
  if(a==1)
  {
    ecran("Environnement trop humide",0)
  }
  else if(a==-1)
  {
    ecran("Environnement trop sec",0)
  }
  else
  {
    ecran("Humidité de la plante optimale",0)
  }
}

float get_moisture_soil()
{
  soilSensor.wakeUp();
  uint16_t = moisture;
  soilSensor.readMoistureRaw(&moisture);
  soilSensor.sleep();
  return (float)moisture;
}

float get_temperature_soil()
{
  soilSensor.wakeUp();
  float temperature;
  soilSensor.readTemperatureCelsius(&temperature);
  soilSensor.sleep();
  return (float)temperature;
}

float get_temperature()
{
  // Reading temperature takes about 250 milliseconds!
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Check if any reads failed and exit early (to try again).
  if (isnan(t))
  {
    Serial.println(F("Failed to read TEMPERATURE from DHT sensor!"));
    return;
  }
  return t;
}

float get_debit() // en Litre
{
  return waterFlow += 1.0 / 5880.0;
}

float get_humidity()
{
  // Reading humidity takes about 250 milliseconds!
  // Read humidity
  float h = dht.readHumidity();
  // Check if any reads failed and exit early (to try again).
  if (isnan(h))
  {
    Serial.println(F("Failed to read HUMIDITY from DHT sensor!"));
    return;
  }
  return h;
}

float get_distance()
{
  // Debut de la mesure avec un signal de 10 µS applique sur TRIG 
  digitalWrite(Broche_Trigger, LOW);    // On efface l'etat logique de TRIG 
  delayMicroseconds(2);
  digitalWrite(Broche_Trigger, HIGH);   // On met la broche TRIG a "1" pendant 10µS 
  delayMicroseconds(10);
  digitalWrite(Broche_Trigger, LOW);    // On remet la broche TRIG a "0" 

  // On mesure combien de temps le niveau logique haut est actif sur ECHO //
  Duree = pulseIn(Broche_Echo, HIGH);

  // Calcul de la distance grace au temps mesure 
  Distance = Duree*0.034/2; // 

  // Verification si valeur mesuree dans la plage //
  if (Distance >= MesureMaxi || Distance <= MesureMini)
  {
    Serial.println("Distance de mesure en dehors de la plage (3 cm à 3 m)");    // erreur si hors plage
    Distance = 777777;
  }
  return Distance;
}

float get_luminosity()
{
  uint16_t irq = veml.interruptStatus();
  if (irq & VEML7700_INTERRUPT_LOW)
  {
    Serial.println("** Low threshold"); 
  }
  if (irq & VEML7700_INTERRUPT_HIGH)
  {
    Serial.println("** High threshold"); 
  }
  delay(500);

  return veml.readLux(); //lumière en LUX
  //return veml.readWhite(); //lumière blanche
  //return veml.readALS(); //lumière ambiante
}

byte get_i2c_address() //Pas utile selon moi
{
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

void ecran(char* name, float value)
{
  Serial.begin(115200);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(2000);
  display.clearDisplay();

  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  // Display static text
  display.println(name, " : %f", value);
  display.display(); 
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