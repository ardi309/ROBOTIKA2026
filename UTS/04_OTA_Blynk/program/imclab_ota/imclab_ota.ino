#include "template_config.h"
#define BLYNK_FIRMWARE_VERSION "1.0.1"  // Target pembaruan OTA via Blynk.Air
#define BLYNK_PRINT Serial
#define USE_ESP32_DEV_MODULE           // Edgent tidak mengambil alih LED GPIO2.
#define APP_DEBUG

#include "ImcCore.h"
bool otaInProgress = false;
void stopForOta();
#define IMCLAB_BEFORE_OTA() stopForOta()
#define IMCLAB_LEAVE_RUNNING() do { motorLocked = true; stopMotor(); } while (0)
#include "BlynkEdgent.h"

void stopForOta() {
  otaInProgress = true;
  motorLocked = true;
  stopMotor();
}

void publishStatus() {
  if (!Blynk.connected()) return;
  Blynk.virtualWrite(V0, rpm);
  Blynk.virtualWrite(V1, appliedPwm());
  Blynk.virtualWrite(V2, requestedPwm);
  Blynk.virtualWrite(V3, motorEnabled ? 1 : 0);
  Blynk.virtualWrite(V4, BLYNK_FIRMWARE_VERSION);
}

BLYNK_CONNECTED() {
  stopMotor();
  publishStatus();
}

BLYNK_WRITE(V2) {
  if (otaInProgress) return;
  requestedPwm = constrain(param.asInt(), 0, 255);
  applyMotor();
}

BLYNK_WRITE(V3) {
  motorEnabled = !motorLocked && !otaInProgress && param.asInt() == 1;
  applyMotor();
}

void motorService() {
  motorLocked = otaInProgress || !Blynk.connected() || BlynkState::get() != MODE_RUNNING;
  if (motorLocked) stopMotor();
  if (sampleRpm()) printStatus("DATA");
}

void setup() {
  Serial.begin(115200);
  beginMotor();
  motorLocked = true;
  Serial.println("iMCLab firmware " BLYNK_FIRMWARE_VERSION);
  edgentTimer.setInterval(50L, motorService);
  edgentTimer.setInterval(1000L, publishStatus);
  BlynkEdgent.begin();
}

void loop() {
  BlynkEdgent.run();
  // Serial dikelola konsol Edgent; kendali motor modul ini melalui dashboard.
}
