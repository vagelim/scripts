#!/usr/bin/env python
#To get twitter oauth tokens
#1. Get your consumer key and consumer secret from the app page on apps.twitter.com
#2. Use the birdy python library

from birdy.twitter import UserClient

key = raw_input("Consumer key: ")
secret = raw_input("Consumer secret: ")
client = UserClient(key, secret)
token = client.get_signin_token()
access_key = token.oauth_token
access_secret = token.oauth_token_secret
print token.auth_url
pin = raw_input("PIN: ")
client = UserClient(key, secret, access_key, access_secret)
client.get_access_token(pin)
print token
