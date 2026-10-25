#pragma once
#include <Arduino.h>
#include <esp_arduino_version.h>

// Pin diambil dari materi/imclab_Blynk_kelas.ino. Verifikasi revisi kit.
constexpr uint8_t LED_PIN = 2;
constexpr uint8_t MOTOR_IN1 = 27;
constexpr uint8_t MOTOR_IN2 = 26;
constexpr uint8_t MOTOR_PWM = 12;
constexpr uint8_t RPM_PIN = 13;
constexpr uint8_t PWM_CHANNEL = 0;
constexpr uint32_t PWM_FREQ = 30000;
constexpr uint8_t PWM_BITS = 8;
constexpr uint32_t PULSES_PER_REV = 2;  // Kalibrasi pada poros yang diukur.
constexpr uint32_t DEBOUNCE_US = 500;

int requestedPwm = 200;
bool motorEnabled = false;
bool motorLocked = false;
float rpm = 0;
uint32_t sampleMs = 0, samplePulses = 0, lastSample = 0;
volatile uint32_t pulseCount = 0, lastPulseUs = 0;
portMUX_TYPE pulseMux = portMUX_INITIALIZER_UNLOCKED;

void IRAM_ATTR pulseISR() {
  uint32_t now = micros();
  portENTER_CRITICAL_ISR(&pulseMux);
  if (uint32_t(now - lastPulseUs) >= DEBOUNCE_US) {
    ++pulseCount;
    lastPulseUs = now;
  }
  portEXIT_CRITICAL_ISR(&pulseMux);
}

int appliedPwm() {
  return motorEnabled && !motorLocked ? requestedPwm : 0;
}

void applyMotor() {
  digitalWrite(MOTOR_IN1, HIGH);
  digitalWrite(MOTOR_IN2, LOW);
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcWrite(MOTOR_PWM, appliedPwm());
#else
  ledcWrite(PWM_CHANNEL, appliedPwm());
#endif
  digitalWrite(LED_PIN, appliedPwm() > 0 ? HIGH : LOW);
}

void stopMotor() {
  motorEnabled = false;
  applyMotor();
}

void beginMotor() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  pinMode(MOTOR_PWM, OUTPUT);
  digitalWrite(MOTOR_PWM, LOW);
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  if (!ledcAttach(MOTOR_PWM, PWM_FREQ, PWM_BITS)) {
    Serial.println("ERR PWM init failed");
    while (true) delay(1000);
  }
#else
  if (ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_BITS) == 0) {
    Serial.println("ERR PWM init failed");
    while (true) delay(1000);
  }
  ledcAttachPin(MOTOR_PWM, PWM_CHANNEL);
#endif
  stopMotor();
  pinMode(RPM_PIN, INPUT_PULLUP);
  lastSample = millis();
  attachInterrupt(digitalPinToInterrupt(RPM_PIN), pulseISR, FALLING);
}

bool sampleRpm() {
  uint32_t now = millis();
  if (uint32_t(now - lastSample) < 1000) return false;
  portENTER_CRITICAL(&pulseMux);
  now = millis();
  samplePulses = pulseCount;
  pulseCount = 0;
  portEXIT_CRITICAL(&pulseMux);
  sampleMs = uint32_t(now - lastSample);
  lastSample = now;
  rpm = samplePulses * 60000.0f / (PULSES_PER_REV * float(sampleMs));
  return true;
}

void printStatus(const char* prefix) {
  Serial.printf("%s PWM=%d SET=%d RPM=%.1f PULSES=%lu DT_MS=%lu\n",
                prefix, appliedPwm(), requestedPwm, rpm,
                (unsigned long)samplePulses, (unsigned long)sampleMs);
}

bool parsePwm(const String& text, int& value) {
  if (text.length() < 1 || text.length() > 3) return false;
  for (unsigned i = 0; i < text.length(); ++i)
    if (text[i] < '0' || text[i] > '9') return false;
  value = text.toInt();
  return value <= 255;
}

void handleCommand(String cmd) {
  cmd.trim();
  if (cmd == "0") {
    stopMotor();
  } else if (cmd == "R" || cmd == "r") {
    printStatus("STATUS");
    return;
  } else if (motorLocked) {
    Serial.println("ERR motor locked");
    return;
  } else if (cmd == "1") {
    if (requestedPwm == 0) requestedPwm = 200;
    motorEnabled = true;
  } else if (cmd == "+" || cmd == "-") {
    requestedPwm = constrain(requestedPwm + (cmd == "+" ? 10 : -10), 0, 255);
  } else if (cmd.startsWith("PWM:")) {
    int value;
    if (!parsePwm(cmd.substring(4), value)) {
      Serial.println("ERR PWM must be 0..255");
      return;
    }
    requestedPwm = value;
  } else {
    Serial.println("ERR use 0, 1, +, -, PWM:0..255, R");
    return;
  }
  applyMotor();
  printStatus("ACK");
}

void pollSerial() {
  static String line;
  static bool overflow = false;
  // Batasi kerja satu iterasi agar servis jaringan tidak terhalang.
  for (int count = 0; count < 64 && Serial.available(); ++count) {
    char c = char(Serial.read());
    if (c == '\r' || c == '\n') {
      if (overflow) Serial.println("ERR line too long");
      else if (line.length()) handleCommand(line);
      line = "";
      overflow = false;
    } else if (!overflow) {
      if (line.length() >= 32) overflow = true;
      else line += c;
    }
  }
}
