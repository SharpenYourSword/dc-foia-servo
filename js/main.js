$.getJSON("https://s3.amazonaws.com/dcfoiaservo/foia.json", function (d) {
  var out = "<h2>FOIA Responses</h2><dl>";
    for (var i in sortObject(d,"pub",false)) {
      var description = d[i].name;
//      var file = d[i].fname + "." + d[i].ftype
      var file = d[i].fname
      var url = "http://code.esq.io/dc-foia-servo/response.html#" + file
      out += '<dt>' + description + '</dt><dd><a href="' + url + '">' + file + '</a></dd><p/>';
    }
    out += '</dl>';
    document.getElementById("foialist").innerHTML=out;

})

function sortObject(obj, prop, asc) {
    obj = obj.sort(function(a, b) {
        if (asc) return (a[prop] > b[prop]) ? 1 : ((a[prop] < b[prop]) ? -1 : 0);
        else return (b[prop] > a[prop]) ? 1 : ((b[prop] < a[prop]) ? -1 : 0);
    });
    console.log()
    return obj
}