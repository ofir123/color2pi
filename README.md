# color2pi
sniffing color using the pi camera, detect median color and send over serial to arduino
## preper pi
1. format and extract noob-lite to SD crap, install raspebian

in raspi-config - enable camera, disable console to serial in "advanced", overclock to turbo


```sudo apt-get update && sudo apt-get upgrade```

```sudo apt-get install python-setuptools```

##install pip and pillow, 
but still stupied jpeg decoder [doesnt load]( http://stackoverflow.com/questions/4632261/pil-jpeg-library-help)

```pip install Pillow```

http://picamera.readthedocs.org/en/release-1.10/quickstart.html

serial disbale logger, if you didnt in the raspi-conf
http://www.irrational.net/2012/04/19/using-the-raspberry-pis-serial-port/

==wish

we will do this all in nodejs, but its too slow and the pi camera seems not to be as well supported

image processing - https://github.com/EyalAr/lwip

camera access - https://github.com/troyth/node-raspicam/

and the p5.js for the visuals
