// Take a PDF file & make JSON out of it.
// USAGE: node app.js -f filename.pdf -o filename.json

var fs = require('fs'),
	path = require('path'),
	exec = require('child_process').exec,
	argv = require('minimist')(process.argv.slice(2));

function run(filename, output) {
	var data = {}

	// check to make sure it's a pdf
	if (path.extname(filename) == ".pdf") {

		// It's a PDF, alright. Let's make a .txt file	
		getTextFromPdf(filename, function (textString)
		{
			data['text'] = textString
			data['filename'] = filename
			if (output == null) {
				console.log(JSON.stringify(data, indent=2))
			}
			else {
				fs.writeFileSync(output, JSON.stringify(data, indent=2))
			}
		})
	}

	// hmm. we're not a PDF. That's too bad.
	else {
		console.log(filename + "is NOT a PDF!")
	}
}

function getTextFromPdf (filename, callback) {
	txtname = filename.replace('.pdf','.txt')
	// if it's a PDF, shell out to `pdftotext -layout -q filename.pdf filename.txt`
	exec('pdftotext -layout ' + filename + " " + txtname, function (err, stdout, stderr) {
		fs.readFile(txtname, function (err, data) {
			exec('rm ' + txtname, function (err, stdout, stderr) {
				callback(data.toString())
			})
		})
	})
}

run(argv.f, argv.o)
