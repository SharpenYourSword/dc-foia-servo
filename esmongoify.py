#!/usr/bin/env python
import pymongo
import os
import json
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from envious import load_env
load_env()

def pushtoDBstores(filename):

	# Initialize ES and Mongo connections
	connection = RequestsHttpConnection
	es = Elasticsearch(connection_class=connection, host=os.environ['BONSAI_HOST'], use_ssl=True, port=int(os.environ["BONSAI_PORT"]))
	client = pymongo.MongoClient(os.environ["MONGOLAB_URI"])
	db = client[os.environ["MONGOLAB_DB"]]
	responses = db['foiaresponses']

	# Open the JSON file
	with open(filename) as f:
		d = json.loads(f.read())
		es.index(index="dcfoiaservo", doc_type="response", body=d)	#load to ES
		responses.insert(d)	#load to MongoLab