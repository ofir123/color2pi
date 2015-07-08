//recives three messages from a python script and reflect it on 3 PWM pins to LEDs

#include <SoftwareSerial.h>
SoftwareSerial mySerial(10, 11); // RX, TX

// pins for the LEDs:
const int redPin = 3;
const int greenPin = 5;
const int bluePin = 6;

void setup() {
  // initialize serial:
  Serial.begin(9600);
  mySerial.begin(9600);

  // make the pins outputs:
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

}

void loop() {
  // if there's any serial available, read it:
  while (mySerial.available() > 0) {
    int red = mySerial.parseInt();
    int green = mySerial.parseInt();
    int blue = mySerial.parseInt();

    blue *= 0.5;
    green *= 0.5;
    
    red = constrain(red, 0 , 255);
    blue = constrain(blue, 0 , 255);
    green = constrain(green, 0 , 255);
    
    if (mySerial.read() == '\n') {
      analogWrite(redPin, red);
      analogWrite(greenPin, green);
      analogWrite(bluePin, blue);
    }

  }
}
