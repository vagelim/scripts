#!/usr/bin/python
from googlevoice import Voice
from googlevoice.util import input
import commands
import sys
import base64 as b64 #Only used if you encode your password to keep from casual perusal
import csv

voice = Voice()
password = b64.b64decode('ENCODED GV PASS')
user = b64.b64decode('ENCODED GV USR')
voice.login(user, password)

phoneNumber = 'CELLPHONE NUMBER (associated with GV account)'

textReader = csv.reader(open('/PATH/TO/PARTY/LIST/party_txt_list.txt','rb'), delimiter=',')

text_list = textReader.next()

def massTXT():
  mass = "massTXT:"
	try:
		text = sys.argv[1]
	except IndexError:
		print "Need message"		
		exit()
	for each in text_list:
		voice.send_sms(each, mass + text)
	

if __name__ == '__main__':
	massTXT()