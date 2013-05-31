#!/usr/bin/python
from googlevoice import Voice
from googlevoice.util import input
import commands
import sys
import base64 as b64 #Only used if you encode your password to keep from casual perusal
import csv
##########
#Program expects two arguments
#1st argument - Message to send (must be in quotes to capture whitespace)
#2nd argument -(OPTIONAL) Path to comma separated file of phone numbers to send to
##########

voice = Voice()
password = b64.b64decode('ENCODED GV PASS')
user = b64.b64decode('ENCODED GV USR')
voice.login(user, password)

phoneNumber = '123-456-7890' #(cell number associated with GV account)

#second argument to program is path to a CSV of phone numbers
try:
	textReader = csv.reader(open(sys.argv[2],'rb'), delimiter=',')
except IndexError:
	#if there is no argument, use hardcoded path
	textReader = csv.reader(open('/PATH/TO/PARTY/LIST/party_txt_list.txt','rb'), delimiter=',')
	#change the above path to a file containing phone numbers separated by commas
text_list = textReader.next()

def massTXT():
	#mass is a string prepended to the text to indicate it is a group message
	#leave blank for no prepended text
  mass = "massTXT:"
  try:
	#program expects text to be first commandline argument to program
	text = sys.argv[1]
  except IndexError:
	print "Need message"		
	exit()
  for each in text_list:
	voice.send_sms(each, mass + text)
	

if __name__ == '__main__':
	massTXT()
