$(document).ready(function() {
  var PORT = 9201; // 4502;
  var s = new WebSocket("ws://localhost:" + PORT + "/");
  var text = $('#text');
  var isConSet = false;
  var prevValue = '';
  var currValue = '';
  
  text.on('input', function() {
    currValue = text.val();

  var dmp = new diff_match_patch();
  var d = dmp.diff_main(prevValue, currValue);
  var ds = dmp.diff_prettyHtml(d);
    var patch_list = dmp.patch_make(prevValue, currValue, d);
  patch_text = dmp.patch_toText(patch_list);
  console.log('patch_text: ', patch_text);
  s.send(patch_text);

  // console.log('d: ', d);
  // console.log('ds: ', ds);
  $('#div').html(ds);
    
    // console.log(currValue);
    if (isConSet) {
      console.log('Sending Value');
    //  s.send(currValue);
    }
    prevValue = currValue;
  });

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

  $('.open-vcs-btn').on('click', function() {
    
  });
});
