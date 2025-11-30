#include <DHT.h>

#define DHTPIN 2 // DHT sensor OUT pin
#define DHTTYPE DHT11
#define PIR_PIN 4  // PIR sensor OUT pin

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  pinMode(PIR_PIN, INPUT);

  // Give PIR time to stabilize
  delay(5000);

  dht.begin();
}

void loop() {
  // Read PIR: HIGH = motion detected
  int motion = digitalRead(PIR_PIN);

  // Read DHT11 temperature + humidity
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // DHT occasionally fails, skip this cycle
  if (isnan(h) || isnan(t)) {
    delay(1000);
    return;
  }

  // Send clean JSON that the Pi parses easily
  Serial.print("{\"temp\":");
  Serial.print(t);
  Serial.print(",\"humid\":");
  Serial.print(h);
  Serial.print(",\"motion\":");
  Serial.print(motion);
  Serial.println("}");

  // Delay it to reduce DB interference
  delay(5000); // 5 seconds
}
