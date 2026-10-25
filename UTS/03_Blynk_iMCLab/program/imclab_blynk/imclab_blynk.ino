#include "secrets.h"
#define BLYNK_PRINT Serial
#include <WiFi.h>
#include <BlynkSimpleEsp32_SSL.h>
#include "ImcCore.h"

BlynkTimer timer;
uint32_t lastConnectAttempt = 0;

void publishStatus() {
  if (!Blynk.connected()) return;
  Blynk.virtualWrite(V0, rpm);
  Blynk.virtualWrite(V1, appliedPwm());
  Blynk.virtualWrite(V2, requestedPwm);
  Blynk.virtualWrite(V3, motorEnabled ? 1 : 0);
}

BLYNK_CONNECTED() {
  // Setpoint lokal dipublikasikan. Status ON lama tidak dipulihkan.
  stopMotor();
  motorLocked = false;
  publishStatus();
}

BLYNK_WRITE(V2) {
  requestedPwm = constrain(param.asInt(), 0, 255);
  applyMotor();
}

BLYNK_WRITE(V3) {
  motorEnabled = !motorLocked && param.asInt() == 1;
  applyMotor();
}

void setup() {
  Serial.begin(115200);
  beginMotor();
  motorLocked = true;
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Blynk.config(BLYNK_AUTH_TOKEN);
  timer.setInterval(1000L, publishStatus);
  Serial.println("READY iMCLab Blynk 1.0.0");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED || !Blynk.connected()) {
    motorLocked = true;
    stopMotor();
    if (WiFi.status() == WL_CONNECTED && millis() - lastConnectAttempt >= 5000) {
      lastConnectAttempt = millis();
      Blynk.connect(3500);
    }
  } else {
    Blynk.run();
    // run() dapat mendeteksi koneksi yang baru putus.
    if (!Blynk.connected()) { motorLocked = true; stopMotor(); }
  }
  pollSerial();
  if (sampleRpm()) printStatus("DATA");
  timer.run();
}
