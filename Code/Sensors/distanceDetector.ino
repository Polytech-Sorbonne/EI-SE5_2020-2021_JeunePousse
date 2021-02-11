#define Broche_Echo 25       // Broche Echo du HC-SR04 sur D25
#define Broche_Trigger 33    // Broche Trigger du HC-SR04 sur D33 


int MesureMaxi = 300; 			// Distance max
int MesureMini = 3; 			// Distance min
long Duree;
long Distance;

void setup()
{
	pinMode(Broche_Trigger, OUTPUT); 	// Broche Trigger en sortie
	pinMode(Broche_Echo, INPUT); 		// Broche Echo en entree
	Serial.begin (115200);
}

void loop() {

	// Debut de la mesure avec un signal de 10 µS applique sur TRIG 

	digitalWrite(Broche_Trigger, LOW); 		// On efface l'etat logique de TRIG 
	delayMicroseconds(2);
	digitalWrite(Broche_Trigger, HIGH); 	// On met la broche TRIG a "1" pendant 10µS 
	delayMicroseconds(10);
	digitalWrite(Broche_Trigger, LOW);		// On remet la broche TRIG a "0" 

	// On mesure combien de temps le niveau logique haut est actif sur ECHO //
	Duree = pulseIn(Broche_Echo, HIGH);

	// Calcul de la distance grace au temps mesure 
	Distance = Duree*0.034/2; // 

	// Verification si valeur mesuree dans la plage //
	if (Distance >= MesureMaxi || Distance <= MesureMini) {
		Serial.println("Distance de mesure en dehors de la plage (3 cm à 3 m)");		// erreur si hors plage
		}
	else {
		// Affichage mesure en serial
		Serial.print("Distance mesuree :");
		Serial.print(Distance);
		Serial.println("cm");
		}
	delay(1000); 
}
