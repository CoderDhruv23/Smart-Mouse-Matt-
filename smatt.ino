#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int touchPin = 3;
bool lastTouchState = LOW;
unsigned long lastTouchTime = 0;
bool doubleTouchDetected = false;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(touchPin, INPUT);
}

void loop() {
  // Read sensors every 2 seconds
  static unsigned long lastRead = 0;
  if (millis() - lastRead > 2000) {
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (!isnan(h) && !isnan(t)) {
      Serial.print("TEMP:");
      Serial.print(t);
      Serial.print(",HUM:");
      Serial.println(h);
    }
    lastRead = millis();
  }

  // Check touch sensor with debouncing and double-touch detection
  bool currentTouchState = digitalRead(touchPin);
  if (currentTouchState != lastTouchState) {
    if (currentTouchState == HIGH) {
      if (millis() - lastTouchTime < 500) {  // Double-touch within 500ms
        Serial.println("TOUCH:SHUTDOWN");
        doubleTouchDetected = true;
      } else {
        Serial.println("TOUCH:WAKE");
      }
      lastTouchTime = millis();
    }
    delay(50); // Debounce delay
    lastTouchState = currentTouchState;
  }
}