#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) return;

  Serial.print("{\"temp\":");
  Serial.print(t);
  Serial.print(",\"humid\":");
  Serial.print(h);
  Serial.println("}");
  delay(2000);
}