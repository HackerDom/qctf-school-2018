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
    }, Math.floor(Math.random() * 120) + 50);
}

textarea.append("<br>");
var socket = new WebSocket("ws://" + window.location.host + "/broadcast");
socket.onmessage = function (event) {
    if (typeof event.data === "string"){
        runner(event.data)
    } else {
        socket.close();
        textarea.append("<br><p style=\"color:red;\">Error! Broadcast has been terminated!</p>");
    }
};



