$(document).ready(function(){
   document.getElementById('textEditor').contentWindow.document.designMode="on";
   document.getElementById('textEditor').contentWindow.document.close();
   var edit = document.getElementById("textEditor").contentWindow;
   edit.focus();
   $("#bold").click(function(){
    if($(this).hasClass("selected")){
     $(this).removeClass("selected");
    }else{
     $(this).addClass("selected");
    }
    boldIt();
   });
   $("#italic").click(function(){
    if($(this).hasClass("selected")){
     $(this).removeClass("selected");
    }else{
     $(this).addClass("selected");
    }
    ItalicIt();
   });
   $("#fonts").on('change',function(){
    changeFont($("#fonts").val());
   });
});
function boldIt(){
 var edit = document.getElementById("textEditor").contentWindow;
 edit.focus();
  edit.document.execCommand("bold", false, "");
  edit.focus();
  // console.log(document.getElementById("textEditor").contentWindow.document.body.innerHTML);
  // document.getElementById("textEditor").contentWindow.document.body.innerHTML = "<b>HELLO</b>";
}
function ItalicIt(){
 var edit = document.getElementById("textEditor").contentWindow;
 edit.focus();
 edit.document.execCommand("italic", false, "");
 edit.focus();
}
function changeFont(font){
 var edit = document.getElementById("textEditor").contentWindow;
 edit.focus();
 edit.document.execCommand("FontName", false, font);
 edit.focus();
}

setInterval(function(){
 var gyt=$("#textEditor").contents().find("body").html().match(/@/g);
 if($("#textEditor").contents().find("body").html().match(/@/g)>=0){}else{
  $("#text").val($("#textEditor").contents().find("body").html());
 }
 $("#text").val($("#textEditor").contents().find("body").html());
},1000);