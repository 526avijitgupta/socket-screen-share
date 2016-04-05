$(document).ready(function() {
  var PORT = 4536; // 4502;
  var SERVER_IP = "192.168.43.190";
  var s = new WebSocket("ws://" + SERVER_IP + ":"  + PORT + "/");
  var fileNameServer = new WebSocket("ws://" + SERVER_IP + ":4510/");

  var text = $('#text');
  var isConSet = false;
  var prevValue = '';
  var currValue = '';
  var filesString = '';

  text.on('input', function() {
    currValue = text.val();

    //var dmp = new diff_match_patch();
    //var d = dmp.diff_main(prevValue, currValue);
    //var ds = dmp.diff_prettyHtml(d);
    //var patch_list = dmp.patch_make(prevValue, currValue, d);
    //patch_text = dmp.patch_toText(patch_list);
    //console.log('patch_text: ', patch_text);
    ///s.send(patch_text);

    // console.log('d: ', d);
    // console.log('ds: ', ds);
    //$('#div').html(ds);
    // console.log(currValue);
    if (isConSet) {
      console.log('Sending Value', currValue);
      s.send(currValue);
    }
    prevValue = currValue;
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
        createFileButtons(files_list);
      }
    } else {
      text.val(value);
    }
  };

  $('.open-vcs-btn').on('click', function() {

  });
});

function createFileButtons(files_list) {
  removeAllFileButtons();

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
      $('.file-buttons').append(btnElem);
      console.log(btnElem);
    }
  });

}

function removeAllFileButtons() {
  $('.file-buttons').empty();
  // $('.file-button').each(function())
}
