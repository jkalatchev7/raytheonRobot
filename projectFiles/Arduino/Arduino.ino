#include <Servo.h> 
#include<IRremote.h>
#include<IRremoteInt.h>

//IR sensor
int irPin = 12;
int LightSens = A3;
int Echo = A4;  
int Trig = A5; 

//180 is left, 0 right
Servo myservo;
Servo holderServo;
IRrecv receiver(irPin);
decode_results results;
int analogValue;
float voltage;
void setup() {
  initializeMotors();
  myservo.attach(3);
  holderServo.attach(13);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.write(0);
  holderServo.write(90);
  pinMode(A4, INPUT);
  pinMode(A5, OUTPUT);


  Serial.begin(9600);
  receiver.enableIRIn();
}

int Distance_test() {
  digitalWrite(Trig, LOW);   
  delayMicroseconds(2);
  digitalWrite(Trig, HIGH);  
  delayMicroseconds(20);
  digitalWrite(Trig, LOW);   
  float Fdistance = pulseIn(Echo, HIGH);  
  Fdistance= Fdistance / 58;       
  return (int)Fdistance;
}  


void serialTranslate() {
  Serial.println("Serial Trans");
  digitalWrite(LED_BUILTIN, HIGH);
  String r = Serial.readString();
  String action = r.substring(0,4);
  
  if (action == "move") {
    int dis = r.substring(5).toInt();
    forwardMotors(255, dis);
    delay(100);
    Serial.println("done");
  } else if (action == "turn") {
    int angle = r.substring(5).toInt();
    turnBot(angle);
    delay(100);
    Serial.println("done");
  } else if (action == "sequ") {
    myservo.write(120);
    delay(200);
    int middleDistance = Distance_test();
    Serial.println("move");
    while (middleDistance >= 20) {
      Serial.println(String(middleDistance));
      delay(50);
      forwardMotors(175);
      middleDistance = Distance_test();
    }
    stopMotors();
    Serial.println("turn");
    delay(600);
    turnBot(100);
    Serial.println("move");
    delay(600);
    forwardMotors(255, 20);
    Serial.println("turn");
    delay(600);
    turnBot(-100);
    Serial.println("done");
  } else if (action == "coll") {
    analogValue = analogRead(A3);
    voltage = analogValue * (5.0 / 1024.0);
    while (voltage > 0.5){
      forwardMotors(100);
    }
    stopMotors();
    holderServo.write(90);
    Serial.println("collected");
  } else {
    Serial.print(r);
  }
  digitalWrite(LED_BUILTIN, LOW);
  /*
  switch(r) {
    case "L":
      turnBot(90);
      break;
    case "R":
      turnBot(-90);
      break;
    default:
      //center();
      break;
  }
  */
}

void irTranslate() {
  switch(IrReceiver.decodedIRData.command) {
    case 70:
      Serial.println("Up");
      Serial.println("move");
      delay(200);
      forwardMotors(255, 12);
      break;
    case 68:
      Serial.println("Left");
      Serial.println("turn");
      delay(200);
      turnBot(-90);
      break;
    case 67:
      Serial.println("Right");
      Serial.println("turn");
      delay(200);
      turnBot(90);
      break;
    case 21:
      Serial.println("Down");
      myservo.write(120);
      break;
    case 64:
      Serial.println("picture");
      break;
    case 22:
      Serial.println("1");
      myservo.write(0);
      turnBot(45);
      break;
    case 25:
      Serial.println("2");
      forwardMotors(255, 20);
      break;
    case 13:
      analogValue = analogRead(A3);
      Serial.println("3");
      myservo.write(0);
      voltage = analogValue * (5.0 / 1024.0);
      while (voltage > 0.5){
        forwardMotors(100);
        analogValue = analogRead(A3);
        voltage = analogValue * (5.0 / 1024.0);
        Serial.println(voltage);
      }

      forwardMotors(50);
      delay(500);
      myservo.write(90);
      delay(500);
      stopMotors();
      break;
    case 12:
      Serial.println("4");
      break;
    case 24:
      Serial.println("5");
      Serial.println("done");
      break;
    case 94:
      Serial.println("6");
      break;
    case 8:
      Serial.println("7");
      analogValue = analogRead(A3);
      myservo.write(120);
      turnBotB(true);
      voltage = analogValue * (5.0 / 1024.0);
      Serial.println(voltage);
      while (voltage > 0.5) {
        analogValue = analogRead(A3);
        voltage = analogValue * (5.0 / 1024.0);
        Serial.println(voltage);
        
      }
      delay(200);
      stopMotors();
      delay(500);
      forwardMotors(150);
      delay(300);
      myservo.write(0);
      delay(300);
      stopMotors();
      
      break;
    case 28:
      Serial.println("8");
      break;
    case 90:
      Serial.println("9");
      myservo.write(0);
      break;
    case 82:
      Serial.println("0");
      break;
    case 66:
      Serial.println("*");
      break;
    case 74:
      Serial.println("#");
      break;
    default:
      break;
  }
}

void loop() {
  
   if (Serial.available() > 0) {
    serialTranslate();
  } else if(IrReceiver.decode()) {
    irTranslate();
    //Serial.println(IrReceiver.decodedIRData.command);
    receiver.resume();
  } else {
    Serial.println("Nothing");
    //Serial.println(String(Distance_test()));
    delay(500);
  }
 
}
