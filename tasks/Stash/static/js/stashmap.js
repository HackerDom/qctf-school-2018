var oReq = new XMLHttpRequest();
oReq.open("GET", "/coordinates.gif", true);
oReq.responseType = "arraybuffer";

oReq.onload = function(oEvent) {
  var arrayBuffer = oReq.response;
  var blob = new Blob([arrayBuffer], {type: "image/gif"});
  $("#map").attr('src', URL.createObjectURL(blob));
};
oReq.send();