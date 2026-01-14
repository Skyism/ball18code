#include <string.h>
#include <Servo.h>

Servo esc;
const int ESC_PIN = 9; // change

const int MIN_US = 1000;  // typical
const int MAX_US = 2000;  // typical

// PINS (edit based on wiring)
const byte step_pin_y = 3; 
const byte dir_pin_y = 2; 
const byte step_pin_x = 5; 
const byte dir_pin_x = 4; 

//max min speed of steppers
const unsigned long MIN_STEP_DELAY_US = 10;   // fastest speed
const unsigned long MAX_STEP_DELAY_US = 500;  // slowest speed

// MOTION (must be tuned)
const long PAN_MAX  = 8000;   // steps from home to max safe pan
const long TILT_MAX = 4000;   // steps from home to max safe tilt

const float GAIN = 2.0f;      // steps per unit dx/dy
const int DEADBAND = 3;       // if dx/dy < deadband, ignore it
const int MAX_STEP_JUMP = 50; // max change to target per message (steps)


// TARGETS
long panTarget = 0;
long tiltTarget = 0;

// Flywheel speed
const int FLYWHEEL_SPEED = 50;

// Constants for reading strings in C
const int SERIAL_BUF_SIZE = 80;
char serialBuf[SERIAL_BUF_SIZE];
int serialPos = 0;
bool lineReady = false;


// Helpers to parse serial communication
// assume message looks like: "isMouthOpen:True;dx:5;dy:10\n"
bool parseField(const String &msg, const char *key, long &out) {
  int k = msg.indexOf(key);
  if (k < 0) return false;
  k += strlen(key);
  int end = msg.indexOf(';', k);
  if (end < 0) end = msg.length();
  out = msg.substring(k, end).toInt();
  return true;
}

bool parseBoolField(const String &msg, const char *key, bool &out) {
  int k = msg.indexOf(key);
  if (k < 0) return false;
  k += strlen(key);
  int end = msg.indexOf(';', k);
  if (end < 0) end = msg.length();
  String v = msg.substring(k, end);
  v.trim();
  out = (v == "1" || v == "true" || v == "True" || v == "TRUE");
  return true;
}

void setup() {
  //Setup Stepper output pins
  pinMode(step_pin_y,OUTPUT); 
  pinMode(dir_pin_y,OUTPUT);
  pinMode(step_pin_x,OUTPUT); 
  pinMode(dir_pin_x,OUTPUT);

  //set up frequency for serial communication
  Serial.begin(115200);

  panTarget = 0;
  tiltTarget = 0;


  esc.attach(ESC_PIN, 1000, 2000);

  esc.writeMicroseconds(MIN_THROTTLE);
  delay(2000);  // most ESCs need 1–2s at min to arm

  Serial.println("ESC armed");
}

void loop() {
  //parse message
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\r') continue;
    if (c == '\n') {
      serialBuf[serialPos] = '\0';  // end string
      lineReady = true;
      serialPos = 0;
    }
    else if (serialPos < SERIAL_BUF_SIZE - 1) {
      serialBuf[serialPos++] = c;
    }
  }

  //if the message is ready
  if (lineReady) {
    
    lineReady = false;

    String line = String(serialBuf);

    bool isMouthOpen = false;
    long dx = 0, dy = 0;

    bool ok1 = parseBoolField(line, "isMouthOpen:", isMouthOpen);
    bool ok2 = parseField(line, "XPos:", dx);
    bool ok3 = parseField(line, "YPos:", dy);

    //if we receive the message well
    if (ok1 && ok2 && ok3) {
      panTarget = dx;
      tiltTarget = dy;
    }
  }

  if (abs(tiltTarget) < DEADBAND) {
    tiltTarget = 0;
  }
  if (abs(panTarget) < DEADBAND) {
    panTarget = 0;
  }

  setStepperSpeedY(deadband(tiltTarget, -.25, .25) * 4);
  setStepperSpeedX(deadband(panTarget, -.25, .25) * 4);

  if (tiltTarget == 0 && panTarget == 0 && isMouthOpen) {
    esc.writeMicroseconds(RUN_THROTTLE);   // run flywheel
  else {
    esc.writeMicroseconds(MIN_THROTTLE);   // stop flywheel
  }

  delay(20); // ~50 Hz update, fine for ESC
  }
}

double deadband(double val, double min, double max){
  if (val < min){
    val = min;
  } else if(val > max){
    val = max;
  }
  return val;
}



void setStepperSpeedY(double Val) {
  static unsigned long lastStepTime = 0;

  if (Val == 0) {
    return; // deadzone, do not step
  }

  // Set direction
  if (Val > 0) {
    digitalWrite(dir_pin_y, HIGH);
  } else {
    digitalWrite(dir_pin_y, LOW);
  }

  // Map |x| from [0,1] to delay range
  double mag = abs(Val);
  unsigned long stepDelay =
    MAX_STEP_DELAY_US -
    (unsigned long)((MAX_STEP_DELAY_US - MIN_STEP_DELAY_US) * mag);

  unsigned long now = micros();
  if (now - lastStepTime >= stepDelay) {
    lastStepTime = now;

    digitalWrite(step_pin_y, HIGH);
    delayMicroseconds(3); // step pulse width
    digitalWrite(step_pin_y, LOW);
  }
}

void setStepperSpeedX(double Val) {
  static unsigned long lastStepTime = 0;

  if (Val == 0) {
    return; // deadzone, do not step
  }

  // Set direction
  if (Val > 0) {
    digitalWrite(dir_pin_x, HIGH);
  } else {
    digitalWrite(dir_pin_x, LOW);
  }

  // Map |x| from [0,1] to delay range
  double mag = abs(Val);
  unsigned long stepDelay =
    MAX_STEP_DELAY_US -
    (unsigned long)((MAX_STEP_DELAY_US - MIN_STEP_DELAY_US) * mag);

  unsigned long now = micros();
  if (now - lastStepTime >= stepDelay) {
    lastStepTime = now;

    digitalWrite(step_pin_x, HIGH);
    delayMicroseconds(3); // step pulse width
    digitalWrite(step_pin_x, LOW);
  }
}
