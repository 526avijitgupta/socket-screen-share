$(document).ready(function() {
  var PORT = 4502;
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
    var value = e.data;
    console.log('Server ' + value);

    if (value.indexOf('Files_List: ') !== -1) {
      value = value.replace('Files_List: ', '');
      var files_list = value.split(' ');
      console.log(files_list);

      files_list.forEach(function(file, index) {
        if (file !== '') {
          var btn = document.createElement('button');
          btn.textContent = file;
          var btnElem = $(btn);
          btnElem.addClass(file);
          btnElem.on('click', function() {
            var clickedFile = $(this).attr('class');
            console.log(clickedFile);
            s.send(clickedFile);
          });
          $('body').append(btnElem);
          console.log(btnElem);
        }
      });
    } else {
      text.val(value);
    }

  };
});
