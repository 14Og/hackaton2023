#include <Servo.h>
#include <Wire.h>



#define S_V 9
#define S_H 10


Servo V;
Servo H;
uint8_t servo_angles[3] {0, 90, 90};

void setup() 
{
  pinMode(S_V, OUTPUT);
  pinMode(S_H, OUTPUT);
  V.attach(S_V);
  H.attach(S_H);
  Wire.begin(0x68);
  Wire.onReceive(receiveEvent);
}
void receiveEvent(int k)
{
  int p = 0;
  while(Wire.available())
  {
   int c = Wire.read();
   servo_angles[p] = c;
   p++; 
  }
}

void servo_i2c(uint8_t hservo, uint8_t vservo)
{
  V.write(vservo);
  H.write(hservo);
}

void loop() {
servo_i2c(servo_angles[1], servo_angles[2]);
}
