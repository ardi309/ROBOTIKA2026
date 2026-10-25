// Modul 01 dan firmware pendamping Python untuk Modul 02.
#include "ImcCore.h"

void setup() {
  Serial.begin(115200);
  beginMotor();
  Serial.println("READY iMCLab basic 1.0.0; newline; 0/1/+/-/PWM:0..255/R");
}

void loop() {
  pollSerial();
  if (sampleRpm()) printStatus("DATA");
}
