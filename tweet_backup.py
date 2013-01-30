#!/bin/python
import sys
import os
import commands

def backup():
    user = sys.argv[1]
    store = sys.argv[2]
    command = "curl -s --user-agent 'Mozilla' --insecure 'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name="
    append = "&page="
    x = 1
    print "This may take a while..."
    tweet_file = open(store, 'a')
    while x < 32:
        tweets = commands.getoutput(command+user+append+str(x) + "'")
        tweet_file.write(tweets)
        x = x + 1
        
    tweet_file.close()

if __name__ == '__main__':
    backup()
