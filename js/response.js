hash = window.location.hash
url = "https://s3.amazonaws.com/dcfoiaservo/json/" + hash.replace("#","") + '.json';
$.getJSON(url, function (data) {
    $("#foiaresponse").append(
      "<h1>" + data.name + "</h1><p>Published: " + data.pub + ". Get original <a href='https://s3.amazonaws.com/dcfoiaservo/" + data.fname + "." + data.ftype + "'>original file</a>.</p><p><pre>" + data.text + "</pre></p>"
    )
  }).fail(function() {
  	$("#foiaresponse").append(
  		"<p>There's no response here. Sorry.</p>"
	)
  })