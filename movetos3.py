#!/usr/bin/env python

import boto
from boto.s3.connection import S3Connection
import os

pwd = os.getcwd()

conn = S3Connection(os.environ["AWS_ACCESS_KEY_ID"], os.environ["AWS_SECRET_ACCESS_KEY"])
b = conn.get_bucket(os.environ["BUCKET_NAME"])
from boto.s3.key import Key

k = b.new_key("foia.json")
k.set_contents_from_filename("foia.json")

for fn in os.listdir(pwd + "/files/"):
	if (b.get_key(fn) == None):
		k = b.new_key(fn)
		k.set_contents_from_filename('files/' + fn)