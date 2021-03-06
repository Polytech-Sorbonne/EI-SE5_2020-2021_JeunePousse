#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>               //Ecran
#include <Adafruit_GFX.h>       //Ecran
#include <Adafruit_SSD1306.h>   //Ecran
#include "DHT.h"                //Capteur temperature
#include "SSD1306Ascii.h"

///////////////////////////////////
#define SOIL_SENSOR_PIN 15   //pin D15
#define Broche_Echo_1 25     // Broche Echo du HC-SR04 distance sur D25
#define Broche_Echo_2 12     // Broche Echo du HC-SR04 eau sur D12
#define Broche_Trigger 33    // Broche Trigger du HC-SR04 sur D33
#define POMPE 18            // commande pompe D18
#define LED 23              //commande leds D23
#define DHTPIN 4
#define DHTTYPE DHT22

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
///////////////////////////////////
DHT dht(DHTPIN, DHTTYPE);

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1); // Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
//Capteur distance
int MesureMaxi = 150;       // Distance max
int MesureMini = 3; // Distance min
long Duree;
long Distance;

const int PINPOMPE = 12;
const int PINLED = 13;
///////////////////////////////////
const char *AP_SSID = "SSID";
const char *AP_PWD = "PWD";

HTTPClient http;

int delay_time_ms;
int mode_auto;

int server_general_portCOM = 8888;
int server_own_portCOM;
const char* SERVER_URL = "http://<your_ip>:";

char SERVER_LINK[80];

struct post_commands{
  const char *first_connexion = "first_connexion";
  const char *kit = "kit_connexion";
  const char *value = "add_measure"; //envoyer les mesures
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

struct post_commands p;
struct server_response server_rep;
struct sensor s;
struct action a;
struct measure m;

//Donnees envoyees par le serveur lors de la premiere connection
char reference[] = "SN2024";
char* nom_kit = "Expert";

int pot_height = 11.5; //en centimetres

//Declarations fonctions
void setup_wifi();
int post_kit_connexion();
StaticJsonDocument<200> send_values();
void lights(int a);
void water_screen(int a);
void temperature_screen(int a);
void humidity_screen(int a);
void ground_screen(int a);
void lum_screen(int a);
void print_demarrage();
float get_temperature();
float get_humidity();
float get_moisture();
void watering(int watering_time);
void lights_on();
void lights_off();
float get_distance();
float get_niveau_eau();
void display_screen(char* text);
void clear_screen();

void setup(){
  byte address;
  Serial.begin(115200);

  Serial.println(F("Debut programme"));


  //setup pompe et panneau LED
  pinMode(PINPOMPE, OUTPUT);
  pinMode(PINLED, OUTPUT);
  Serial.println(F("Setup pompe"));

  //setup luminosite
  while(!Serial)
  {
    delay(10);
  }
  Serial.begin(115200);

  //setup Distance
  pinMode(Broche_Trigger, OUTPUT);  // Broche Trigger en sortie
  pinMode(Broche_Echo_1, INPUT);    // Broche Echo_1 en entree
  pinMode(Broche_Echo_2, INPUT);    // Broche Echo_2 en entree
  Serial.println(F("Setup broches"));

  //setup Ecran
  print_demarrage();
  Wire.begin();
  Serial.println(F("Setup Ecran"));

  //setup sol
  pinMode(SOIL_SENSOR_PIN,INPUT);
  Serial.println(F("Setup Sol"));

  //setup pompe
  pinMode(POMPE, OUTPUT);

  //setup lumiere
  pinMode(LED, OUTPUT);
  lights_on();

  //setup Temperature et Humidity
  dht.begin();

  //setup WiFi
  setup_wifi();

  //setup all
  int a = post_kit_connexion();
  Serial.println(a);
  Serial.println("Fin setup");
}

void loop(){

  StaticJsonDocument<200> resp;

  Serial.println("Debut loop");
  if ((WiFi.status() == WL_CONNECTED)) {

    //Mesure des valeurs
    m.Temperature = get_temperature();
    m.Humidity = get_humidity();
    m.GroundQuality = get_moisture();
    m.WaterLevel = get_niveau_eau();
    clear_screen();
    delay(3000);
    resp = send_values();

    if(resp == NULL){
      Serial.println("Erreur, envoi des valeurs");//ERREUR
    }

  }
  else{
    Serial.println("Connection lost...\n");
    setup_wifi();
  }
  delay(delay_time_ms);
}

//Connecte l'ESP32 au point d'acces Wi-Fi
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

//Envoie au serveur la reference du module et le nom du kit, afin d'avoir un nouveau
//port de communication
int post_kit_connexion(){

  StaticJsonDocument<200> doc;
  StaticJsonDocument<200> resp;

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Debut post_kit_connexion");
    HTTPClient http;

    sprintf(SERVER_LINK, "%s%d/%s", SERVER_URL, server_general_portCOM, p.kit);
    http.begin(SERVER_LINK);
    Serial.println(SERVER_LINK);
    doc["Reference"] = reference;
    doc["kit_name"] = nom_kit;

    String json_body;
    serializeJson(doc, json_body);
    Serial.println(json_body);

    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = 0;
    httpResponseCode = http.POST(json_body);

    Serial.print("Code reponse : ");
    Serial.println(httpResponseCode);
    if(httpResponseCode > 0){

      String response = http.getString();
      Serial.println(response);
      deserializeJson(resp, response);

      //on met a jour le port de communication propre a ce systeme
      server_own_portCOM = atoi(resp["PortCOM"]);
      Serial.println(server_own_portCOM);
      http.end();
      Serial.println("Fin post_kit_connexion");
      return 0;
    }
  }
  return 1;
}

StaticJsonDocument<200> send_values(){

  StaticJsonDocument<200> doc;
  StaticJsonDocument<200> resp;

  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    sprintf(SERVER_LINK, "%s%d/%s", SERVER_URL, server_own_portCOM, p.value);
    Serial.println(SERVER_LINK);
    http.begin(SERVER_LINK);
    http.addHeader("Content-Type", "application/json");

    //on met les valeurs de chaque capteur
    doc["Reference"] = reference;
    doc[s.Temperature] = m.Temperature;
    doc[s.Humidity] = m.Humidity;
    doc[s.GroundQuality] = m.GroundQuality;
    doc[s.WaterLevel] = m.WaterLevel;
    doc[s.Luminosity] = m.Luminosity;

    String requestBody;
    serializeJson(doc, requestBody);
    Serial.println(requestBody);
    int httpResponseCode = http.POST(requestBody);
    Serial.println(httpResponseCode);


    String response = http.getString();
    Serial.println(response);
    deserializeJson(resp, response);
    //Serial.println(resp);

    //Valeurs renvoyées par le serveur

    mode_auto = resp["mode"];
    delay_time_ms = resp["delay"];

    if(mode_auto == 1){
      clear_screen();
      delay(3000);
      temperature_screen(resp["temp_indicator"]);
      delay(3000);
      humidity_screen(resp["hum_indicator"]);
      delay(3000);
      ground_screen(resp["grnd_indicator"]);
      delay(3000);
      water_screen(resp["water_indicator"]);
      //Allume ou eteint les lumieres
      lights(resp["light_power"]);
      //Arrose les plantes
      watering(resp["irrig_score"]);

    }
    else if(mode_auto == -1){
      display_screen("JeunePousse");
      delay(500);
      display_screen(reference);
      delay(500);
    }

  }
  else{
    doc.clear();
  }
  return doc;
}

void lights(int a){
  if(a == 1)
    lights_on();
  else
    lights_off();
}

void water_screen(int a){
  if(a==-1)
  {
    display_screen("Niveau d'eau TRES faible");
  }
  else if(a==1)
  {
    display_screen("Niveau d'eau optimale");
  }
  else
  {
    display_screen("Niveau d'eau faible");  }
}

void temperature_screen(int a){
  if(a==-1){
    display_screen("La plante a froid");
  }
  else if(a==1){
    display_screen("La plante a chaud");
  }
  else{
    display_screen("Temp. plante optimale");
  }
}

void humidity_screen(int a){
  if(a==1){
    display_screen("Environnement trop humide");
  }
  else if(a==-1){
    display_screen("Environnement trop sec");
  }
  else{
    display_screen("Humidite optimale");
  }
}

void ground_screen(int a){
  if(a==1){
    display_screen("Sol trop humide");
  }
  else if(a==-1){
    display_screen("Sol trop sec");
  }
  else{
    display_screen("Humidite du sol optimale");
  }
}

void lum_screen(int a){
  if(a == 0){
    display_screen("Luminosite suffisante.");
  }
  else if(a == -1){
    display_screen("Luminisite insuffisante.");
  }
}

//Premier affichage pour mettre en place l'ecran
void print_demarrage()
{
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  display.println("Demarrage ... ");
  display.println("Bienvenue jeune pousse!");
  display.display();
  delay(3000);
  display.clearDisplay();
  delay(3000);
  display.setCursor(0, 10);
}


//Renvoie la temperature mesuree par le capteur
float get_temperature(){
  float t = dht.readTemperature();
  return t;
}

//Renvoie l'humidite dans l'air mesuree par le capteur
float get_humidity(){
  float h = dht.readHumidity();
  return h;
}

//Renvoie l'humidite du sol mesuree par le capteur
float get_moisture(){
  float moisture = analogRead(SOIL_SENSOR_PIN);
  return moisture;
}

//Arrose la plante
void watering(int watering_time){
    digitalWrite(POMPE,HIGH);
    delay(watering_time*1000);
    digitalWrite(POMPE,LOW);
  }

//Allume la lumiere
void lights_on(){
  digitalWrite(LED,HIGH);
  }

//Eteins la lumiere
void lights_off(){
  digitalWrite(LED,LOW);
}

//Renvoie la distance de la personne par rapport au po
float get_distance(){
  digitalWrite(Broche_Trigger, LOW);     // On efface l'etat logique de TRIG
  delayMicroseconds(2);
  digitalWrite(Broche_Trigger, HIGH);   // On met la broche TRIG a "1" pendant 10µS
  delayMicroseconds(10);
  digitalWrite(Broche_Trigger, LOW);    // On remet la broche TRIG a "0"
  Duree = pulseIn(Broche_Echo_1, HIGH);
  delay(500);
  float d = Duree*0.034/2;
  return d;
  }

//Renvoie le niveau d'eau restant en pourcentage
float get_niveau_eau(){

  digitalWrite(Broche_Trigger, LOW);     // On efface l'etat logique de TRIG
  delayMicroseconds(2);
  digitalWrite(Broche_Trigger, HIGH);   // On met la broche TRIG a "1" pendant 10µS
  delayMicroseconds(10);
  digitalWrite(Broche_Trigger, LOW);    // On remet la broche TRIG a "0"
  float Duree_eau = pulseIn(Broche_Echo_2, HIGH);
  //Serial.print("Duree_eau : ");
  //Serial.println(Duree_eau);
  float Distance_eau = Duree_eau*0.034/2;
  float d_eau = ((pot_height-Distance_eau)/pot_height)*100.0;
  return d_eau;

 }

//Affiche text sur l'ecran
void display_screen(char * text){

  display.println(text);
  display.display();

}

//Efface le texte sur l'ecran
void clear_screen(){

  display.clearDisplay();
  display.setCursor(0, 10);

 }
