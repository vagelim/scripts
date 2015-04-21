#!/usr/bin/env python

#Parse list of artists from villagevoice concert page

import requests
from BeautifulSoup import BeautifulSoup, Comment

r = requests.get('http://www.villagevoice.com/concerts/')

bs = BeautifulSoup(r.text)

spans = bs.findAll('span')
artists = []

for each in spans:
	if str(each).find('name') != -1:
		each = str(each)
		#If there is a name element
		content_location = each.find('content') + len('content=\"')
		end = each.find('">')
		name = each[content_location:end]
		if name != '':
			artists.append(each[content_location:end])
	
