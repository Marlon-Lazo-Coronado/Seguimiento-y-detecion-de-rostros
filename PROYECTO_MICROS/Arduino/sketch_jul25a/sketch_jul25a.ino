/*
    CODIGO PARA ARDUINO
    Mueve un servo segun el valor recibido por Serial
*/
#include <Servo.h>
#define SERX 3 //Pin para el servo X
#define SERY 4 //Pin para el servo Y
 
Servo servoX; //Objeto servo
Servo servoY;
int mssg; //Variable para guardar el mensaje recibido por serial
  
void setup()
{
   //Inicializamos el servo y el Serial:
   servoX.attach(SERX);
   servoY.attach(SERY);
   Serial.begin(9600);
   servoY.write(90);
   servoX.write(0);
}
  
void loop()
{


    
     if (Serial.available() > 0)
   {
      
     mssg = Serial.parseInt(); //Leemos el serial

       // mssg = mssg - 180;


        servoY.write(mssg);
        Serial.println(mssg);

        servoX.write(mssg); //Movemos el servo
        Serial.println(mssg);

     
   }
}
