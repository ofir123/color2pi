//see readme and run following on the pc 
//npm install zmq servi
// node color2web.js

//color sensor to  webpage background



///////////  servi function  ////////////
///////////////////////////////////////////
var latestData = 0;
var servi = require('servi');
var app = new servi(false); // servi instance
app.port(8080);             // port number to run the server on
 
// configure the server's behavior:
app.serveFiles("public");     // serve static HTML from public folder
app.route('/data', sendData); // route requests for /data to sendData()
// now that everything is configured, start the server:
app.start();

function sendData(ServiRequest) {
  // print  that a client HTTP request came in to the server:
  console.log("Got a client request, sending them the data.");
  // respond to the client request with the latest serial string:
  ServiRequest.respond(latestData);
}

//////// ZMQ ////////
var zmq = require('zmq');
// socket to talk to clients
var zmqResponder = zmq.socket('rep');
zmqResponder.on('message', function(request) {
  console.log("Received request: [", request.toString(), "]");
 
  setTimeout(function() {
    latestData = request.toString();
    // send reply back to client.
    zmqResponder.send("OK");
  }, 1000);
 
});

zmqResponder.bind('tcp://*:5556', function(err) {
  if (err) {
    console.log(err);
  } else {
    console.log("Listening on 5556");
  }
});

process.on('SIGINT', function() {
  zmqResponder.close();
});
//used to move things, back when we worked with serial
//serialPort.on('data', saveLatestData);
function saveLatestData(data) {
   console.log(data);
   latestData = data;
}
