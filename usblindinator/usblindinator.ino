// The Blindinator v1.0 by Ivan Cooper & Meena Shah
// created for San Francisco Science Hack Day 2014

#include <DigiUSB.h>
#include <SimpleServo.h>

SimpleServo servo_x; // create servo object to control a servo
SimpleServo servo_y; // create servo object to control a servo
const int servo_x_pin = 1; // pin on which the servo is attached
const int servo_y_pin = 0; // pin on which the servo is attached
const int light_pin = 2;

int x_pos=90;
int y_pos=90;
int light_status=LOW;

int state=0;
int in;
int next_x;

void setup() {      
  DigiUSB.begin();  
  pinMode(light_pin, OUTPUT);
  servo_x.attach( servo_x_pin ); // attaches the servo on the defined pin to the servo object
  servo_y.attach( servo_y_pin ); // attaches the servo on the defined pin to the servo object
}

void loop() {
  if(DigiUSB.available() > 0) {
    in = DigiUSB.read();
    switch(state) {
    case 0:
      if(in == '.') {
        light_status=LOW;
        state=1;
      } else if(in == '*') {
        light_status=HIGH;
        state=1;
      } else if(in>='0' && in<=('0'+180)) {
        // possible dropped character, treat this as X value
        next_x = (in-'0');
        state=2;
      } 
      // else invalid symbol, ignore
      break;
    case 1: // positioning x
      if(in>='0' && in<=('0'+180)) {
        next_x = (in-'0');
        state=2;
      } else if(in == '*') {
        // possible dropped character, try to recover
        light_status=HIGH;
      } else if(in == '.') {
        // possible dropped character, try to recover
        light_status=LOW;
      } else {
        // invalid symbol, reset
        state=0;
      }
      break;
    case 2:
      if(in>='0' && in<=('0'+180)) {
        // got complete position, store and reset
        x_pos = next_x;
        y_pos = (in-'0');
        state=0;
      } else if(in == '*') {
        // possible dropped character, try to recover
        light_status=HIGH;
        state=1;
      } else if(in == '.') {
        // possible dropped character, try to recover
        light_status=LOW;
        state=1;
      } else {
        // invalid symbol, reset
        state=0;
      }
      break;  
    default:
      // invalid state means corrupt RAM, but what the heck, try to recover
      state=0;
      break; 
    }
  }
  digitalWrite(light_pin,light_status);
  servo_x.write(x_pos);
  servo_y.write(y_pos);
  DigiUSB.delay(10);
}
