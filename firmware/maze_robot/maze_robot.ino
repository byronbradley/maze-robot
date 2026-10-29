#include <Arduino.h>
#include "Planner.h"

// Pin assignments match hardware/wiring.md. Commands are PWM duty, not speed.
constexpr uint8_t LEFT_IN1 = 3, LEFT_IN2 = 5, RIGHT_IN1 = 6, RIGHT_IN2 = 9;
constexpr uint8_t SLEEP_PIN = 10, FAULT_PIN = 11, HOLD_TO_RUN = 12;
constexpr uint8_t TRIG[3] = {2, 4, 7};  // front, left, right
constexpr uint8_t ECHO[3] = {A0, A1, A2};
constexpr bool MOTION_CALIBRATED = false;
constexpr bool INVERT_LEFT = false, INVERT_RIGHT = false;
constexpr int DRIVE_PWM = 80, TURN_PWM = 75, MAX_PWM = 120;
constexpr uint32_t CELL_MS = 1500, QUARTER_TURN_MS = 550;
constexpr uint32_t PING_GAP_MS = 65, ECHO_TIMEOUT_US = 25000, MAX_AGE_MS = 260;
constexpr float WALL_CM = 20.0f, FRONT_STOP_CM = 8.0f, SIDE_KP = 2.0f;

volatile uint32_t echoRise = 0, echoWidth = 0;
volatile bool echoDone = false, echoHigh = false;
volatile int8_t activeSensor = -1;
struct Range { float cm = 0; uint32_t stamp = 0; bool valid = false; } ranges[3];
uint32_t pingStartedUs = 0, lastPingMs = 0, stateStarted = 0;
uint32_t waitingSince = 0;
uint8_t nextSensor = 0, pendingHeading = 0, turnSteps = 0;
bool started = false;
Planner planner;
enum class State { IDLE, SENSE, TURN, SETTLE, DRIVE, DONE, FAULT };
State state = State::IDLE;

void edge(uint8_t sensor) {
  if (activeSensor != sensor) return;
  if (digitalRead(ECHO[sensor])) { echoRise = micros(); echoHigh = true; }
  else if (echoHigh) { echoWidth = micros() - echoRise; echoDone = true; echoHigh = false; }
}
void frontEdge() { edge(0); }
void leftEdge() { edge(1); }
void rightEdge() { edge(2); }

void bridge(uint8_t in1, uint8_t in2, int command) {
  command = constrain(command, -MAX_PWM, MAX_PWM);
  // Clear both inputs before changing direction. Zero selects coast.
  analogWrite(in1, 0); analogWrite(in2, 0);
  if (command > 0) analogWrite(in1, command);
  else if (command < 0) analogWrite(in2, -command);
}
void motors(int left, int right) {
  bridge(LEFT_IN1, LEFT_IN2, INVERT_LEFT ? -left : left);
  bridge(RIGHT_IN1, RIGHT_IN2, INVERT_RIGHT ? -right : right);
}
void disableDriver() { digitalWrite(SLEEP_PIN, LOW); motors(0, 0); }
void stopWithFault(const char *reason) {
  disableDriver(); state = State::FAULT; started = false;
  Serial.print("FAULT: "); Serial.println(reason);
}
void invalidateRanges() { for (auto &range : ranges) range.valid = false; }
bool fresh(uint8_t i) { return ranges[i].valid && millis() - ranges[i].stamp <= MAX_AGE_MS; }
bool allFresh() { return fresh(0) && fresh(1) && fresh(2); }

void serviceSonar() {
  uint32_t now = millis();
  if (activeSensor >= 0) {
    noInterrupts();
    bool done = echoDone;
    uint32_t width = echoWidth;
    interrupts();
    if (!done && micros() - pingStartedUs < ECHO_TIMEOUT_US) return;
    uint8_t sensor = activeSensor;
    noInterrupts(); activeSensor = -1; echoDone = false; echoHigh = false; interrupts();
    ranges[sensor].stamp = now;
    ranges[sensor].cm = width * 0.0343f / 2.0f;
    ranges[sensor].valid = done && width >= 116 && width <= 23324;
  }
  if (now - lastPingMs < PING_GAP_MS) return;
  uint8_t sensor = nextSensor;
  nextSensor = (nextSensor + 1) % 3;
  noInterrupts(); echoDone = false; echoHigh = false; echoWidth = 0; activeSensor = sensor; interrupts();
  pingStartedUs = micros(); lastPingMs = now;
  digitalWrite(TRIG[sensor], HIGH); delayMicroseconds(10); digitalWrite(TRIG[sensor], LOW);
}

void beginSensing() {
  motors(0, 0); state = State::SETTLE; stateStarted = millis();
}
void planStep() {
  if (!allFresh()) {
    if (millis() - waitingSince > 1200) stopWithFault("no complete valid wall scan");
    return;
  }
  planner.observe(planner.heading, ranges[0].cm < WALL_CM);
  planner.observe((planner.heading + 3) % 4, ranges[1].cm < WALL_CM);
  planner.observe((planner.heading + 1) % 4, ranges[2].cm < WALL_CM);
  Serial.print("cell "); Serial.print(planner.row); Serial.print(','); Serial.println(planner.col);
  if (planner.atGoal()) { disableDriver(); state = State::DONE; Serial.println("GOAL"); return; }
  int direction = planner.nextDirection();
  if (direction < 0) { stopWithFault("no route"); return; }
  pendingHeading = direction;
  turnSteps = (pendingHeading + 4 - planner.heading) % 4;
  if (turnSteps) {
    state = State::TURN; stateStarted = millis();
  } else if (planner.confirmedOpen(planner.heading)) {
    state = State::DRIVE; stateStarted = millis();
  } else stopWithFault("unconfirmed forward passage");
}

void setup() {
  pinMode(SLEEP_PIN, OUTPUT); digitalWrite(SLEEP_PIN, LOW);
  for (uint8_t pin : {LEFT_IN1, LEFT_IN2, RIGHT_IN1, RIGHT_IN2}) pinMode(pin, OUTPUT);
  pinMode(FAULT_PIN, INPUT_PULLUP); pinMode(HOLD_TO_RUN, INPUT_PULLUP);
  analogWriteResolution(8); disableDriver();
  for (uint8_t i = 0; i < 3; ++i) {
    pinMode(TRIG[i], OUTPUT); digitalWrite(TRIG[i], LOW); pinMode(ECHO[i], INPUT);
  }
  attachInterrupt(digitalPinToInterrupt(ECHO[0]), frontEdge, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ECHO[1]), leftEdge, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ECHO[2]), rightEdge, CHANGE);
  Serial.begin(115200); planner.reset();
}

void loop() {
  serviceSonar();
  while (Serial.available()) {
    char command = Serial.read();
    if (command == 's') { stopWithFault("serial stop; reset physical pose before r"); }
    if (command == 'r') { disableDriver(); started = false; planner.reset(); state = State::IDLE; }
    if (command == 'g' && state == State::IDLE) {
      if (!MOTION_CALIBRATED) Serial.println("Set measured motion constants before enabling g.");
      else if (digitalRead(HOLD_TO_RUN) != LOW) Serial.println("Hold run button before g.");
      else if (!allFresh()) Serial.println("Waiting for valid front/left/right ranges.");
      else {
        started = true; digitalWrite(SLEEP_PIN, HIGH);
        // DRV8833 wake-up time is allowed by the subsequent settle interval.
        beginSensing();
      }
    }
    if (command == 'p') {
      for (uint8_t i = 0; i < 3; ++i) {
        Serial.print(i); Serial.print(':');
        if (fresh(i)) Serial.println(ranges[i].cm); else Serial.println("invalid/stale");
      }
    }
  }
  if (!started) return;
  if (digitalRead(HOLD_TO_RUN) != LOW) { stopWithFault("run button released; pose requires reset"); return; }
  if (digitalRead(FAULT_PIN) == LOW) { stopWithFault("driver fault"); return; }
  uint32_t elapsed = millis() - stateStarted;
  switch (state) {
    case State::SETTLE:
      if (elapsed >= 150) {
        invalidateRanges(); waitingSince = millis(); state = State::SENSE;
      }
      break;
    case State::SENSE: planStep(); break;
    case State::TURN: {
      if (!allFresh()) { stopWithFault("sensor loss during turn"); break; }
      uint32_t duration = QUARTER_TURN_MS * (turnSteps == 2 ? 2 : 1);
      if (elapsed >= duration) { planner.heading = pendingHeading; beginSensing(); }
      else if (turnSteps == 3) motors(-TURN_PWM, TURN_PWM);
      else motors(TURN_PWM, -TURN_PWM);
      break;
    }
    case State::DRIVE:
      if (!allFresh()) { stopWithFault("sensor loss during drive; pose uncertain"); break; }
      if (ranges[0].cm <= FRONT_STOP_CM) { stopWithFault("front clearance; pose uncertain"); break; }
      if (elapsed >= CELL_MS) { motors(0, 0); planner.arrived(); beginSensing(); }
      else {
        int correction = 0;
        if (ranges[1].cm < WALL_CM && ranges[2].cm < WALL_CM)
          correction = constrain(int(SIDE_KP * (ranges[2].cm - ranges[1].cm)), -25, 25);
        motors(DRIVE_PWM + correction, DRIVE_PWM - correction);
      }
      break;
    default: disableDriver(); started = false; break;
  }
}
