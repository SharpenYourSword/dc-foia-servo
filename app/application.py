from flask import Flask, render_template, request, json
import requests
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
#	return "hello world"

@app.route("/response/<docid>/")
def foia_response(docid):
	with open('/home/vzvenyach/Coding/dcfoiaservo/json/' + docid + '.json') as f:
		obj = json.load(f)
	return render_template('response.html', jsonobj=obj)

@app.route("/search/")
def search():
	pass

if __name__ == "__main__":
    app.run(debug=True)