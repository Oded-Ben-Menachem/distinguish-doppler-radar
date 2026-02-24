#include <Arduino.h>
#include <vector>
#include <WiFi.h>

/* Pointer Declaration:
   'hw_timer_t' is a structure that represents the hardware timer.
   The '*' means this is a pointer. It will hold the memory address 
   of the timer we initialize in setup().
*/
hw_timer_t * MyTimer = NULL; 
const int Arr_size = 1024;
volatile uint16_t Arry1[Arr_size];
volatile uint16_t Arry2[Arr_size];
volatile int sampleIndex = 0;
volatile bool Arry1Ready = false;
volatile bool Arry2Ready = false;
volatile int ActiveArry = 1;
int numberOfSample = 0;
const int totalNumOfSample = 100;

const int voltage_pin = 34;
const int Sample_pin = 14;
const int Led_pin1 = 33;
const int Led_pin2 = 32;
// The interpt function
//'ARDUINO_ISR_ATTR' ensures this code is stored in IRAM (fast RAM)
//   so the CPU can jump to it instantly without lag.
void ARDUINO_ISR_ATTR onTimer(){
  uint16_t sample =  analogRead(Sample_pin);
  if (ActiveArry == 1){
    Arry1[sampleIndex] = sample;
  }
  else{
    Arry2[sampleIndex] = sample;
  }
  sampleIndex ++;
  if (sampleIndex == Arr_size - 1){
    if (ActiveArry == 1){
      ActiveArry = 2;
      Arry1Ready = true;
    }
    else{
      ActiveArry = 1;
      Arry2Ready = true;
    }
    sampleIndex = 0;
  }
  
}


void setup() {
Serial.begin(921600);
pinMode(voltage_pin,OUTPUT);
pinMode(Sample_pin, INPUT);
pinMode(Led_pin1, OUTPUT);
pinMode(Led_pin2, OUTPUT);
WiFi.mode(WIFI_OFF);

/*  timerBegin(timer_num, prescaler, count_up):
       - '0': Use Hardware Timer 0.
       - '80': The Prescaler. The ESP32 clock is 80MHz. 
          80MHz / 80 = 1MHz, so 1 timer tick = 1 microsecond (1us).
       - 'true': Count upwards.
 */

MyTimer = timerBegin(0,80,true);

/*  timerAttachInterrupt(timer, function_address, edge_type):
    - '&onTimer': Pass the memory address of our ISR function.
    - 'true': Use edge-triggered interrupt.
*/

timerAttachInterrupt(MyTimer, &onTimer, true);

/* timerAlarmWrite(timer, ticks, autoreload):
   - '200': Set the alarm to trigger every 200 ticks.
   Since 1 tick = 1us, 200us interval = 5,000 Hz (5kHz).
   - 'true': Automatically reset the timer (Reload) after each alarm.
    */

timerAlarmWrite(MyTimer,200,true);
/* timerAlarmEnable(timer):
   Explicitly enable the alarm to start generating interrupts.
    */
timerAlarmEnable(MyTimer);

}

void loop() {
  //digitalWrite(Led_pin1, HIGH);
  if (Arry1Ready == true){
    Serial.write(0xAA);
    Serial.write(0xBB);
    Serial.write((uint8_t*)Arry1,Arr_size * 2);
    
    Serial.write(0xCC);
    Serial.write(0xDD);
    Arry1Ready = false;
    }
  
  if (Arry2Ready == true){
    Serial.write(0xAA);
    Serial.write(0xBB);
    Serial.write((uint8_t*)Arry2,Arr_size * 2);
    
    Serial.write(0xCC);
    Serial.write(0xDD);
    Arry2Ready = false;
    }
  }


  


