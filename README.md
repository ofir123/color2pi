# color2pi
sniffing color using the pi camera  to python  
detect avrage color using pillow
send over serial to arduino   
send over zqm to a node server running a p5.js html file.

## preper pi
1. format and extract noob-lite to SD crap, install raspebian

in raspi-config - enable camera, disable console to serial in "advanced", overclock to turbo


```sudo apt-get update && sudo apt-get upgrade```

```sudo apt-get install python-setuptools```

##install pip and pillow
```pip install Pillow```
http://picamera.readthedocs.org/en/release-1.10/quickstart.html



==node 
came from [another git](https://github.com/shenkarSElab/Adafruit_TCS34725/tree/master/examples/colorview/node-serialport)

*zmq* is explained [here](http://zguide.zeromq.org/page:all)  
 The REQ-REP socket pair is in lockstep. The client issues zmq_send() and then zmq_recv(), in a loop (or once if that's all it needs). Doing any other sequence (e.g., sending two messages in a row) will result in a return code of -1 from the send or recv call. Similarly, the service issues zmq_recv() and then zmq_send() in that order, as often as it needs to.
 
 the client is color2pi.py  
 the server is color2web.js / deviantArt.py  
 
== for pi ==
needs some trickery to get  node/zmq going on pi
```wget http://node-arm.herokuapp.com/node_latest_armhf.deb ```
```sudo dpkg -i node_latest_armhf.deb```  
via [thi guy](http://weworkweplay.com/play/raspberry-pi-nodejs/)

and then the node npm package   
```npm install zmq servi```

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


====last res====
https://www.npmjs.com/package/osc-min  
https://github.com/colinbdclark/osc.js-examples/tree/master/nodejs
