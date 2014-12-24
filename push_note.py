#!/usr/bin/env python
#Obtain your API_KEY from: https://www.pushbullet.com/account

from pushbullet import PushBullet
import sys

API_KEY = "YOUR API KEY HERE"

pb = PushBullet(API_KEY)

if __name__ == "__main__":

	if len(sys.argv) > 3:#If the message being passed is not encapsulated in quotes, it will be broken at each whitespace into separate arguments
		sys.argv[2] = ' '.join(sys.argv[1:])

	success, push = pb.push_note(sys.argv[1], sys.argv[2])
	print success
