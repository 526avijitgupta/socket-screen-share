$(document).ready(function() {
  var PORT = 4540; // 4502;
  var FILES_PORT = 4511;
  var PREDICTION_PORT = 4500;
  var SERVER_IP = "localhost";
  var s = new WebSocket("ws://" + SERVER_IP + ":"  + PORT + "/");
  var fileNameServer = new WebSocket("ws://" + SERVER_IP + ":" + FILES_PORT + "/");
  var prediction_engine = new WebSocket("ws://" + SERVER_IP + ":" + PREDICTION_PORT + "/");
  // var text = $('#textEditor');
  var isConSet = false;
  var prevValue = '';
  var currValue = '';
  var filesString = '';

  $(document).ready(function(){
      function getCaretCharacterOffsetWithin(element) {
          var doc = element.ownerDocument || element.document;
          var win = doc.defaultView || doc.parentWindow;
          var sel, range, preCaretRange, caretOffset = 0;
          if (typeof win.getSelection != "undefined") {
              sel = win.getSelection();
              if (sel.rangeCount) {
                  range = sel.getRangeAt(0);
                  preCaretRange = range.cloneRange();
                  preCaretRange.selectNodeContents(element);
                  preCaretRange.setEnd(range.endContainer, range.endOffset);
                  caretOffset = preCaretRange.toString().length;
              }
          } else if ( (sel = doc.selection) && sel.type != "Control") {
              range = doc.selection.createRange();
              preCaretRange = doc.body.createTextRange();
              preCaretRange.moveToElementText(element);
              preCaretRange.setEndPoint("EndToEnd", textRange);
              caretOffset = preCaretTextRange.text.length;
          }
          return caretOffset;
      }
      $('body', $('#textEditor').contents()).on('input', function(e) {
  // alert('testing');
        // console.log(e)
        console.log("typing")
        currValue = $("#textEditor").contents().find("body").html();
        if (currValue.length > prevValue.length){

          var iframe = document.getElementById("textEditor");
          var iframeBody = (iframe.contentDocument || iframe.contentWindow.document).body;
          var cursor_position = getCaretCharacterOffsetWithin(iframeBody);
          var extracted_string = currValue.substring(0,cursor_position);
          var split_string = extracted_string.split(" ");
          var split_string_len = split_string.length;
          if (split_string_len > 2) {
            var array_bigram = split_string.slice(split_string_len - 3, split_string_len-1);
            var prefix = split_string[split_string_len-1];
            // console.log(array_bigram);
            // console.log(prefix);
            prediction_engine.send(array_bigram.join(" ") + "&" + prefix);
          }else{
            if(split_string_len == 2){
              var array_bigram = split_string.slice(split_string_len - 2, split_string_len-1);
              var prefix = split_string[split_string_len-1];
              // console.log(array_bigram);
              // console.log(prefix);
              prediction_engine.send(array_bigram.join(" ") + "&" + prefix);
            }
          }
        }

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


  prediction_engine.onopen = function() {
    console.log('prediction server open');
  };
  prediction_engine.onclose = function(error) {
    console.log('Websocket error ' + error);
    prediction_engine.send("connection closed");
  };
  prediction_engine.onmessage = function(e) {
    var value = e.data;
    console.log(value);
    var availableTags = value.split("&");
    // $( "#textEditor" ).autocomplete({
    //   source: availableTags
    // });
    console.log(availableTags)
    var datalist = document.getElementById('names');
    datalist.textContent = '';
    for (var i = 0; i < availableTags.length; i++) {
        var option = document.createElement('option');
        option.text = availableTags[i];
        option.onclick = function() { console.log($(this).val());
          function getCaretCharacterOffsetWithin(element) {
              var doc = element.ownerDocument || element.document;
              var win = doc.defaultView || doc.parentWindow;
              var sel, range, preCaretRange, caretOffset = 0;
              if (typeof win.getSelection != "undefined") {
                  sel = win.getSelection();
                  if (sel.rangeCount) {
                      range = sel.getRangeAt(0);
                      preCaretRange = range.cloneRange();
                      preCaretRange.selectNodeContents(element);
                      preCaretRange.setEnd(range.endContainer, range.endOffset);
                      caretOffset = preCaretRange.toString().length;
                  }
              } else if ( (sel = doc.selection) && sel.type != "Control") {
                  range = doc.selection.createRange();
                  preCaretRange = doc.body.createTextRange();
                  preCaretRange.moveToElementText(element);
                  preCaretRange.setEndPoint("EndToEnd", textRange);
                  caretOffset = preCaretTextRange.text.length;
              }
              return caretOffset;
          }
          var currValue = $("#textEditor").contents().find("body").html();
          var iframe = document.getElementById("textEditor");
          var iframeBody = (iframe.contentDocument || iframe.contentWindow.document).body;
          var cursor_position = getCaretCharacterOffsetWithin(iframeBody);
          var prefixextracted_string = currValue.substring(0,cursor_position);
          var suffixextracted_string = currValue.substring(cursor_position, currValue.length);
          var split_extracted_string = prefixextracted_string.split(" ");
          split_extracted_string[split_extracted_string.length - 1] = $(this).val();
          prefixextracted_string = split_extracted_string.join(" ");
          var value = prefixextracted_string + suffixextracted_string;
          $("#textEditor").contents().find("body").html(value);
          var edit = document.getElementById("textEditor").contentWindow;
          edit.focus();
          s.send(value);
        };
        datalist.appendChild(option);
    }

  }



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
      var edit = document.getElementById("textEditor").contentWindow;
      edit.focus();
    }
  };

  $('.open-vcs-btn').on('click', function() {

  });
});

