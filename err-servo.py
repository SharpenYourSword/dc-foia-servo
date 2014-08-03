#!/usr/bin/env python

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import re
from pyvirtualdisplay import Display
import requests
from requests.exceptions import Timeout
import json
import subprocess
from twitterservo import tweetIt
#import tweetaboutit

dl = os.getcwd() + "/files/"
saved = json.loads(open("foia.json").read())
exists = []
for responses in saved:
	exists.append(responses.get("fname"))

def checkNewFile(fname):
	for r in exists:
		if r == fname:		# Check to see if File exists
			return False	# File already exists!
	return True

def download_file(url, cookiedict, fname, ftype, description, pub_date):

	local_filename = "files/" + fname + "." + ftype
	if (os.path.exists(local_filename)):
		return local_filename
	elif checkNewFile(fname): # Check to see if File exists
		print "Hey, this is a new file: " + local_filename 
		viewstate = cookiedict["ASP.NET_SessionId"] + "_3"
		new_url = "https://foia-dc.gov/ERR/palEleViewDocs.aspx?__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&CUSTOMVIEWSTATE_KEY=VIEWSTATE_" + viewstate + "&__VIEWSTATE=&pageno=1&relpath=&hiddocid=&hidisPalDoc=F&hidDocTypes=3%2C4%2C5%2C66%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21%2C22%2C23%2C64%2C24%2C25%2C26%2C27%2C28%2C29%2C30%2C31%2C32%2C33%2C34%2C35%2C36%2C37%2C38%2C39%2C40%2C41%2C68%2C69%2C74%2C70%2C72%2C73%2C71%2C42%2C43%2C44%2C45%2C46%2C47%2C48%2C49%2C50%2C51%2C52%2C53%2C54%2C55%2C56%2C57%2C58%2C59%2C60%2C61%2C62%2C63%2C78%2C79&txtDocName=*&txtContent=&hidflg=Y&txtFrom=&txtTo=&pgNo=1&hidsrt=0&hidsrtfield=2&hidNoMoreVisibility=True&hiderrid=" + fname
		try:
			r = requests.post(new_url, cookies=cookiedict, stream=True, timeout=1.001)
			with open(local_filename, 'wb') as fd:
				for chunk in r.iter_content(chunk_size=4096):
					fd.write(chunk)

			# convert it to a json object
			done = subprocess.call(["node bin/reports.js -f " + local_filename + " -o json/" + fname + ".json"], shell=True)
			
			# Take existing metadata and file and add it all together
			f = open("json/" + fname + ".json")
			d = json.load(f)
			f.close()
			with open("json/" + fname + ".json", 'wb') as jsonobj:
				d["fname"] = fname
				d["description"] = description
				d["ftype"] = ftype
				d["pub"] = pub_date
				d["url"] = "https://s3.amazonaws.com/dcfoiaservo/" + fname + "." + ftype
				jsonobj.write(json.dumps(d, indent=4))

			# When you're here, it's time to tweet about it!
			tweetIt(description, fname, ftype)

		except Timeout:
			print "huh? the download timed out"
	return local_filename

def parse_rows(rows):
	out = []
	i = 1
	while i < len(rows):
		cols = rows[i].find_elements_by_xpath('td')
		f_meta = {}
		if (cols[0].get_attribute("colspan") != "5"):	#Ignore the bottom page
			f_meta["name"] = cols[0].text
			f_meta["pub"] = cols[1].text
			f_meta["pages"] = cols[2].text
			f_meta["size"] = cols[4].text

			fileinfo = cols[3].find_element_by_xpath('a')
			file_link = re.search("(\')(\d+)(\')", fileinfo.get_attribute("href"))
			fname = file_link.group(2)
			f_meta["fname"] = fname
			f_meta["ftype"] = os.path.basename(fileinfo.find_element_by_xpath("img").get_attribute("src")).split(".")[0]
			out.append(f_meta)
		else:
			break
		i += 1
	return out

display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Firefox()
link = "https://foia-dc.gov/ERR/palEleScrRslts.aspx"
driver.get(link)

while(link == driver.current_url):
  time.sleep(1)

driver.switch_to_frame("two");

out = []
cookies = dict()
still_more = True
while (still_more):
	all_cookies = driver.get_cookies()
	for s_cookie in all_cookies:
		cookies[s_cookie["name"]]=s_cookie["value"]
	res = driver.find_elements_by_xpath('//*[@id="frmscrslts"]/table[2]/tbody/tr[3]/td/table[1]/tbody/tr')
	objs = parse_rows(res)

	out += objs
	for obj in objs:
		f = download_file("https://foia-dc.gov/Request/palContentType.aspx?type=3&DocID=" + obj["fname"] + "&isPALDoc=F", cookies, obj["fname"], obj["ftype"], obj["name"], obj["pub"])
	try:
		next_pg = driver.find_element_by_xpath('//*[@id="image15"]')
		next_pg.click()
	except NoSuchElementException:
		still_more = False
		continue

with open("foia.json", 'wb') as fd:
  fd.write(json.dumps(out, indent=4))

import movetos3
print "All Done"