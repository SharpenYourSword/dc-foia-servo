$.getJSON("https://s3.amazonaws.com/dcfoiaservo/foia.json", function (d) {
  var out = "<h2>FOIA Responses</h2><dl>";
    for (var i in d) {
      var description = d[i].name;
      var file = d[i].fname + "." + d[i].ftype
      var url = "https://s3.amazonaws.com/dcfoiaservo/" + file
      out += '<dt>' + description + '</dt><dd><a href="' + url + '">' + file + '</a></dd><p/>';
    }
    out += '</dl>';
    document.getElementById("foialist").innerHTML=out;

})