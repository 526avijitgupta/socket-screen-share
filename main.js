$(document).ready(function() {
    var PORT = 4501
    var s = new WebSocket("ws://localhost:" + PORT + "/");
    var text = $('#text');
    var isConSet = false;
    text.on('input', function() {
	var value = text.val();
	console.log(value);
	if (isConSet) {
	    console.log('Sending Value');
	    s.send(value);
	}
  });

        s.onopen = function() { 
            console.log('Onload');
	    isConSet = true;
          s.send('message sent from client'); 
         };
        
         s.onclose = function(error) {
          console.log('Websocket error ' + error);
         };

         s.onmessage = function(e) {
         	console.log('Server ' + e.data);
         };
});
