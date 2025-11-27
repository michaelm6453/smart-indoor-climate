#include <DHT.h>

// ------------------------
// PIN DEFINITIONS
// ------------------------
#define PIR_PIN 4        // PIR output on D4
#define DHTPIN 2         // DHT11 data pin
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

int lastMotionState = LOW;

void setup() {
  Serial.begin(9600);

  pinMode(PIR_PIN, INPUT);

  Serial.println("Initializing sensors...");
  delay(5000); // to get motion sensor ready
  dht.begin();
}

void loop() {

  // -------- PIR READING --------
  int motion = digitalRead(PIR_PIN);
  String motionText;

  if (motion == HIGH) {
    motionText = "motion detected";
  } else {
    motionText = "no motion";
  }

  // -------- DHT11 READING --------
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Sensor error");
    delay(1000);
    return;
  }

  // -------- JSON OUTPUT --------
  Serial.print("{\"temp\":");
  Serial.print(t);
  Serial.print(",\"humidity\":");
  Serial.print(h);
  Serial.print(",\"");
  Serial.print(motionText);
  Serial.println("\"}");

  delay(1000);
}
