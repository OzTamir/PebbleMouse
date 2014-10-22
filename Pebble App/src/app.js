/**
 * Pebble Mouse v0.1
 * Written by Oz Tamir
 * Website: http://www.oztamir.com
 * The Code for the server can be found here:
 * http://www.github.com/OzTamir/PebbleMouse
 * This is where you write your app.
 */
var UI = require('ui');
var Vector2 = require('vector2');
var Accel = require('ui/accel');

// Used to run this code from app.js
var mainFunc = function(ip) {
var isRunning = false;

var main = new UI.Card({
  title: 'Pebble Mouse',
  subtitle: 'Server: Not connected',
  body: 'Looking for the server...',
  style: 'mono'
});

main.show();
Accel.init();
Accel.config({rate : 100});

var connection = new WebSocket('ws://' + ip + ':8000');

connection.onopen = function () {
  connection.send('0');
  main.subtitle("Server: Waiting for data");
  main.body('Press Select to start sending data to the server.');
};

Accel.on('data', function(e) {
  if (isRunning) {
    connection.send(JSON.stringify(e.accels));
  }
});

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
  main.title("Error");
  main.body("Couldn't connect to the server, please make sure it's running.");
};

connection.onclose = function (e) {
  main.title("Error");
  main.subtitle("Server: Closed");
  main.body("The Server disconnected. Please reset both this app and the server to continue.");
};

main.on('click', 'select', function(e) {
  if (isRunning || connection.readyState == 3) {
    isRunning = false;
    main.body('Currently not running. Press Select to start.');
  }
  else {
    isRunning = true;
    main.subtitle("Server: Running");
    main.body("Stop: Press Select\nLeft Click: Press Up\nRight Click: Press Down");
  }
});

main.on('click', 'up', function(e) {
  if (isRunning || connection.readyState == 3) {
   connection.send("1"); 
  }
});

main.on('click', 'down', function(e) {
  if (isRunning || connection.readyState == 3) {
   connection.send("2"); 
  }
});
  
};

// -----------------------------------


// Load a basic screen
var wind = new UI.Window(); 
var textfield = new UI.Text({
  position: new Vector2(0, 50),
  size: new Vector2(144, 80),
  font: 'gothic-28-bold',
  text: "Set Server IP",
  textAlign: 'center'
});
wind.add(textfield);
var ip = ["192", "168", "0", "0"];
var current = 0;

var count = new UI.Text({
  position: new Vector2(0, 100),
  size: new Vector2(144, 60),
  font: 'gothic-24-bold',
  text: "192",
  textAlign: 'center'
});
wind.add(count);
wind.show();

wind.on('click', 'up', function() {
  ip[current] = (parseInt(ip[current]) + 1).toString();
  count.text(ip[current]);
});

wind.on('click', 'down', function() {
  ip[current] = (parseInt(ip[current]) - 1).toString();
  count.text(ip[current]);
});
 
wind.on('click', 'select', function() {
  if (current < 3) {
    current += 1;
    count.text(ip[current]);
  }
  else {
    var ipString = ip.join(".");
    wind.hide();
    mainFunc(ipString);
  }
});