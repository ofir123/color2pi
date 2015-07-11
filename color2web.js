//see readme and run following on the pc 
//npm install zmq servi
// node color2web.js

//color sensor to  webpage background

var zmq = require('zmq');
// socket to talk to clients
var responder = zmq.socket('rep');


var latestData = 0;
var servi = require('servi');
var app = new servi(false); // servi instance
app.port(8080);             // port number to run the server on
 
// configure the server's behavior:
app.serveFiles("public");     // serve static HTML from public folder
app.route('/data', sendData); // route requests for /data to sendData()
// now that everything is configured, start the server:
app.start();

responder.on('message', function(request) {
  console.log("Received request: [", request.toString(), "]");

  // do some 'work'
  setTimeout(function() {

    // send reply back to client.
    responder.send("World");
  }, 1000);
});


// ZMQ funcs
responder.bind('tcp://*:5556', function(err) {
  if (err) {
    console.log(err);
  } else {
    console.log("Listening on 5555…");
  }
});

process.on('SIGINT', function() {
  responder.close();
});



//used to move things, back when we worked with serial
function saveLatestData(data) {
   //console.log(data);
   latestData = data;
}
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

//serialPort.on('data', saveLatestData);