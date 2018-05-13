var textarea = $('.term');
var i = 0;


function runner(text) {
  textarea.append(text.charAt(i));
  i++;
  setTimeout(
    function() {
      if (i < text.length)
        runner(text);
      else {
        textarea.append("<br>");
        i = 0;
      }
    }, Math.floor(Math.random() * 70) + 30);
}


function strip(str, remove) {
  while (str.length > 0 && remove.indexOf(str.charAt(0)) !== -1) {
    str = str.substr(1);
  }
  while (str.length > 0 && remove.indexOf(str.charAt(str.length - 1)) !== -1) {
    str = str.substr(0, str.length - 1);
  }
  return str;
}

textarea.append("<br>");

var ws_protocol = "ws://";
if (window.location.protocol === "https:")
    ws_protocol = "wss://";

var socket = new WebSocket(ws_protocol + window.location.host + "/" + strip(window.location.pathname, "/") + "/broadcast");
socket.onmessage = function (event) {
    if (typeof event.data === "string"){
        runner(event.data)
    } else {
        socket.close();
        textarea.append("<br><p style=\"color:red;\">Error! Broadcast has been terminated!</p>");
    }
};



