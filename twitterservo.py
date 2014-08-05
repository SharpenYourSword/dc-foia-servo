#!/usr/bin/env python
import twitter
import os

def tweetIt (description, fname, ftype):
	api = twitter.Api(consumer_key=os.environ["TW_CONSUMER_KEY"], consumer_secret=os.environ["TW_CONSUMER_SECRET"], access_token_key=os.environ["TW_TOKEN"],access_token_secret=os.environ["TW_TOKEN_SECRET"])
	if len(description) > 99:
		description = description[:99]
#	out_text = "New posting: " + description[:99] + " https://s3.amazonaws.com/dcfoiaservo/" + fname + "." + ftype
#	When we've converted existing PDFs to JSON, then turn this on!
	out_text = "New posting: " + description[:99] + " http://dc-foia-servo.herokuapp.com/response/" + fname
	status = api.PostUpdate(out_text)
