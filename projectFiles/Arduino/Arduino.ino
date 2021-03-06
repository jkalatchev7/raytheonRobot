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
  holderServo.write(20);
  pinMode(LED_BUILTIN, OUTPUT);
  myservo.write(90);
  pinMode(A4, INPUT);
  pinMode(A5, OUTPUT);

    
   Serial.begin(9600);
   Serial.println("restart");
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
  String r = Serial.readString();
  Serial.println(r);
  String action = r.substring(0,4);
  if (action == "move") {
    int dis = r.substring(5).toInt();
    forwardMotors(255, dis * 12);
    Serial.println("done");
  } else if (action == "turn") {
    int angle = r.substring(5).toInt();
    turnBot(angle);
    delay(900);
    Serial.println("done");
  } else if (action == "sequ") {



      myservo.write(250);              
      delay(1000); 

      forwardMotors(240);
      delay (100);
 
      bool card = false;  
      while (card == false){
 
        float leftDistance = Distance_test();
      
        if (leftDistance <=50){
          delay(500);
          stopMotors();
          card == true;
          break;
          
        }
       else if (leftDistance > 50) { 
          forwardMotors(240);
       }
      }
      Serial.println("done");
     
} else if (action == "seqb") {
    myservo.write(90);
    delay(200);
    int middleDistance = Distance_test();
    while (middleDistance >= 20) {
      Serial.println(String(middleDistance));
      delay(50);
      forwardMotors(255);
      middleDistance = Distance_test();
    }
    
    Serial.println("throwBall");

    stopMotors();
    holderServo.write(35);
    delay(500);
    holderServo.write(110);
    reverseMotors(255, 12);
    holderServo.write(20);
    Serial.println("done");
} else if (action == "seqc") { 
    myservo.write(-10);              
    delay(1000); 
    bool Nothing = false;  
while (Nothing == false){
 
      float leftDistance = Distance_test();
      
     if (leftDistance > 40){
        delay(500);
        stopMotors();
       
        Serial.println("done");
        Nothing = true;        
      }
       else if (leftDistance <= 40) {
        
        forwardMotors(255);
      }

  }


    

  } else if (action == "coll") {
    holderServo.write(20);
    float dis = r.substring(5).toFloat();
    forwardMotors(200, int(dis * 15));
    holderServo.write(113);
    forwardMotors(200, 1);
    Serial.println("done");
  } else if (action == "turR") {
    turnBotB(true);
    while (Serial.available() == 0) {
      Serial.print(Serial.available());
    }

    stopMotors();
    Serial.println("done");
  } else if (action == "turL") {
    turnBotB(false);
    while (Serial.available() == 0) {
      Serial.print(Serial.available());
    }

    stopMotors();
    delay(100);
    Serial.println("done");
  } else if (action == "forw") {
    forwardMotors(200);
    while (Serial.available() == 0) {
      Serial.print(Serial.available());
    } 
    stopMotors();
  } else if (action == "armU") {
    holderServo.write(115);
    delay(200);
  } else if (action == "armD") {
    holderServo.write(35);
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
      myservo.write(90);
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
      holderServo.write(45);
      delay(100);
      holderServo.write(75);
      delay(100);
      holderServo.write(110);
      break;
    case 24:
      Serial.println("5");
      forwardMotors(255);
      delay(700);
      holderServo.write(35);
      stopMotors();
      delay(500);
 
      holderServo.write(20);
      
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
      myservo.write(10);
      delay(500);
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
   
    //Serial.println(String(Distance_test()));
    delay(100);
  }
 
}
