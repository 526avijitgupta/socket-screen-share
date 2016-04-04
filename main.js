$(document).ready(function() {
    var PORT = 4500;
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
    };
    
    s.onclose = function(error) {
        console.log('Websocket error ' + error);
    };
    
    s.onmessage = function(e) {
        console.log('Server ' + e.data);
	text.val(e.data);
    };

    newFile = function() {
	console.log('newfile function called');
	var fileName = prompt("Enter file name","filename.txt");
	if(fileName != null) {
	    console.log(fileName);
	    $.get("http://localhost:5000/file?postfile=" + fileName, function(results){
		console.log(results);
	    });
	}
    }
});
