#include <Servo.h>
#include <Wire.h>


#define R_DIR 4
#define R_PWM 5
#define L_DIR 7
#define L_PWM 6
#define TACH_L 2
#define TACH_R 3
#define S_V 9
#define S_H 10

Servo SERVO_V;
Servo SERVO_H;
int angle_v = 90;
int angle_h = 90;
uint8_t speed[3] {0,128, 128};

void setup() {
Serial.begin(9600);
pinMode(R_DIR, OUTPUT);
pinMode(R_PWM, OUTPUT);
pinMode(L_DIR, OUTPUT);
pinMode(L_PWM, OUTPUT);
pinMode(TACH_L, INPUT);
pinMode(TACH_R, INPUT);
pinMode(S_V, INPUT);
pinMode(S_H, INPUT);
SERVO_V.attach(S_V);
SERVO_H.attach(S_H);
SERVO_H.write(90);
SERVO_V.write(90);
Wire.begin(0x22);
Wire.onReceive(receiveEvent);

}

void drive(uint8_t l_p, uint8_t r_p)
{
  if (l_p == 128)
    analogWrite(L_PWM, 0);
  else if(l_p > 128)
  {
    digitalWrite(L_DIR, HIGH);
    analogWrite(L_PWM, (l_p-128)*2);
  }
  else
  {
    digitalWrite(L_DIR, LOW);
    analogWrite(L_PWM, (128 - l_p)*2-1);
  }
  if (r_p == 128)
    analogWrite(R_PWM, 0);
  else if(r_p > 128)
  {
    digitalWrite(R_DIR, HIGH);
    analogWrite(R_PWM, (r_p-128)*2);
  }
  else
  {
    digitalWrite(R_DIR, LOW);
    analogWrite(R_PWM, (128 - r_p)*2-1);
  }
  



}
void loop() {
  void receiveEvent()
{
  int p = 0;
  while(Wire.available())
    {
      int c = Wire.read();
      speed[p] = c;
      p++;
    }
}
  drive(speed[1], speed[2]);

}
