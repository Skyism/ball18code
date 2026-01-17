#include <WiiChuck.h>

Accessory nunchuck1;

double y = 0;
double x = 0;
bool c = false;
bool z = false;

const byte step_pin_y = 3; /Users/samyuktaathreya/Documents/Arduino/Ball18_Test/Ball18_Test.ino
const byte dir_pin_y = 2; 
const byte step_pin_x = 5; 
const byte dir_pin_x = 4; 

const unsigned long MIN_STEP_DELAY_US = 10;   // fastest speed
const unsigned long MAX_STEP_DELAY_US = 500;  // slowest speed

void setup() {
  Serial.begin(9600);
  nunchuck1.begin();
	nunchuck1.type = NUNCHUCK;
  Serial.println("Starting");

  pinMode(step_pin_y,OUTPUT); 
  pinMode(dir_pin_y,OUTPUT);
  pinMode(step_pin_x,OUTPUT); 
  pinMode(dir_pin_x,OUTPUT);
}


void loop() {
	nunchuck1.readData();
  z = nunchuck1.values[10] >= 127.5;
  c = nunchuck1.values[11] >= 127.5;
  x = ((double)nunchuck1.values[0] / 127.5) - 1.0;
  y = (((double)nunchuck1.values[1] / 127.5) - 1.0);
  
  if(abs(x) < .1){
      x = 0;
  }
  if(abs(y) < .1){
     y = 0;
  }
  

  setStepperSpeedY(y);
  setStepperSpeedX(x);
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
