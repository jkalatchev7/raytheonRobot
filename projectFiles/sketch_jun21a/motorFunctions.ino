int MAX_SPEED = 255;

//Motor A connections
int enA = 5;
int in1 = 7;
int in2 = 8;
// Motor B connections
int enB = 6;
int in3 = 11;
int in4 = 9;
int count = 0;


void initializeMotors() {
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  stopMotors();
  Serial.println("Motors initialized");
}

void stopMotors() {

  // Turn off motors
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void forwardMotors(int speed, int dis) {
  analogWrite(enA, speed);
  analogWrite(enB, speed);
  // Turn on motor A & B
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  delay(dis * 1000 / 25);
  stopMotors();
}

void forwardMotors(int speed) {
  analogWrite(enA, speed + 25);
  analogWrite(enB, speed - 25);
  // Turn on motor A & B
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}


void reverseMotors(int speed, int dis) {
  analogWrite(enA, speed);
  analogWrite(enB, speed);
  // Turn on motor A & B but in reverse
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  delay(dis * 1000 / 25);
  stopMotors();
}

void turnBot(int angle) {
  Serial.println("Turning motors");
  analogWrite(enA, 200);
  analogWrite(enB, 150);

  if (angle > 0) {

    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    delay(angle * 7);
    stopMotors();
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    delay(angle * -6.5);
    stopMotors();
  }
}
