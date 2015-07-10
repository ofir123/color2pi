//see readme and run following on the pc 
//npm install node-serialport servi
// node color2web.js
//and upload color2web.ino onto your arduino

//color sensor to  webpage background
// also check the well written node-serialport intro at https://itp.nyu.edu/physcomp/labs/labs-serial-communication/lab-serial-communication-with-node-js/

var serialport = require('serialport'),// include the library
   SerialPort = serialport.SerialPort, // make a local instance of it
   portName = process.argv[2];    // get port name from the command line:
   portName = "COM15"; //i cheat

var myPort = new SerialPort(portName, {
   baudRate: 9600,
   // look for return and newline at the end of each data packet:
   parser: serialport.parsers.readline("\r\n")
 });

var latestData = 0;
var servi = require('servi');
var app = new servi(false); // servi instance
app.port(8080);             // port number to run the server on
 
// configure the server's behavior:
app.serveFiles("public");     // serve static HTML from public folder
app.route('/data', sendData); // route requests for /data to sendData()
// now that everything is configured, start the server:
app.start();

function sendData(request) {
  // print out the fact that a client HTTP request came in to the server:
  console.log("Got a client request, sending them the data.");
  // respond to the client request with the latest serial string:
  request.respond(latestData);
}

function showData(result) {
  var resultString = result[0];
  text.html("Sensor reading:" + resultString);
  // split it:
  var numbers = split(resultString, " ");
  // use the numbers:
  text.position(numbers[0], numbers[1]);
  text.style("font-size", numbers[2] + "%");
 }

myPort.on('data', saveLatestData);

function saveLatestData(data) {
   //console.log(data);
   latestData = data;
}



function showPortOpen() {
   console.log('port open. Data rate: ' + myPort.options.baudRate);
}
 
function showPortClose() {
   console.log('port closed.');
}
 
function showError(error) {
   console.log('Serial port error: ' + error);
}