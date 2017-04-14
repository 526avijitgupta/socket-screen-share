$(document).ready(function() {
  var PORT = 4540; // 4502;
  var FILES_PORT = 4511;
  var SERVER_IP = "localhost";
  var s = new WebSocket("ws://" + SERVER_IP + ":"  + PORT + "/");
  var fileNameServer = new WebSocket("ws://" + SERVER_IP + ":" + FILES_PORT + "/");

  // var text = $('#textEditor');
  var isConSet = false;
  var prevValue = '';
  var currValue = '';
  var filesString = '';

  $(document).ready(function(){
        $('body', $('#textEditor').contents()).on('input', function(e) {
    // alert('testing');
          console.log("typing")
          currValue = $("#textEditor").contents().find("body").html();
          if (isConSet) {
            console.log('Sending Value', currValue);
            s.send(currValue);
          }
          prevValue = currValue;
        });

  });

  var create = $('#create');
  create.on('click', function() {
    var fileName = prompt('Enter the file name:');
    // console.log('File NAme:', fileName);
    console.log('Create file:', fileName);
    if (fileName) {
      fileNameServer.send('Create file:' + fileName);
    }
  });

  fileNameServer.onopen = function() {
    console.log('File handling server open');
  };

  s.onopen = function() {
    console.log('Onload');
    isConSet = true;
    // s.send('ABC');
  };

  s.onclose = function(error) {
    console.log('Websocket error ' + error);
    s.send("connection closed");
  };

  s.onmessage = function(e) {
    var value = e.data;
    console.log('Server ' + value);

    if (value.indexOf('Files_List: ') !== -1) {
      if (filesString !== value) {
        filesString = value;
        value = value.replace('Files_List: ', '');
        var files_list = value.split(' ');
        console.log(files_list);

        $('.file-buttons').empty();

        files_list.forEach(function(file, index) {
          if (file !== 'empty') {
            var btn = document.createElement('button');
            btn.textContent = file;
            var btnElem = $(btn);
            btnElem.addClass(file);
            btnElem.on('click', function() {
              var clickedFile = $(this).attr('class');
              console.log(clickedFile);
              s.send(clickedFile);
            });
            $('.file-buttons').append(btnElem);
            console.log(btnElem);
          }else{
            $('.file-buttons').empty();
          }
        });
      }
    } else {
      console.log('Sending to textareaL: ', value);
      // text.html(value);
      // document.getElementById("textEditor").contentWindow.document.body.innerHTML = value;
      // $("#textEditor").contents().find("body").html("");
      $("#textEditor").contents().find("body").html(value);
    }
  };

  $('.open-vcs-btn').on('click', function() {

  });
});

