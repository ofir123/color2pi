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


==node 
came from [another git](https://github.com/shenkarSElab/Adafruit_TCS34725/tree/master/examples/colorview/node-serialport)



== for windows (WIP)==

===download===
get git for windows (comes with msys), this will be your command line.
get [nodejs for windows](http://blog.teamtreehouse.com/install-node-js-npm-windows)
go to command line at Adafruit_TCS34725\examples\colorview\node-serialport\color2web

0. run this line to get all the needed packages for node to run this thing
$ npm install zmq servi
1. upload color2pi.ino to arduino
2. run with the node command 
$ node color2web.js COM15
3. open browser at localhost:8080
4. refresh page to get new data

