# color2pi
sniffing color using the pi camera, detect median color and send over serial to arduino
## preper pi
1. format and extract noob-lite to SD crap, install raspebian

in raspi-config - enable camera, disable console to serial in "advanced", overclock to turbo


```sudo apt-get update && sudo apt-get upgrade```

```sudo apt-get install python-setuptools git iceweasel```  
iceweasel is [firefox](https://wiki.debian.org/Iceweasel/), needed if your running selenium (deviantArt.py) 

##install python depends
but still stupied jpeg decoder [doesnt load]( http://stackoverflow.com/questions/4632261/pil-jpeg-library-help)

```sudo pip install Pillow logbook zmq selenium```  
zmq takes long time to compile...

http://picamera.readthedocs.org/en/release-1.10/quickstart.html

serial disbale logger, if you didnt in the raspi-conf
http://www.irrational.net/2012/04/19/using-the-raspberry-pis-serial-port/

##run
```git clone https://github.com/shenkarSElab/color2pi.git```  
```cd color2pi```  
```python color2pi.py localhost 5555```  

==wish

we will do this all in nodejs, but its too slow and the pi camera seems not to be as well supported

see efort [here](https://github.com/shenkarSElab/Adafruit_TCS34725/tree/master/examples/colorview/node-serialport)

image processing - https://github.com/EyalAr/lwip

camera access - https://github.com/troyth/node-raspicam/

and the p5.js for the visuals
