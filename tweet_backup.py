#!/bin/python
import sys
import os
import commands

def clean_tweets(tweets):
    tweet_file = open(tweets, 'r')
    dirty = tweet_file.read()
    tweet_file.close()

    occur = dirty.count('<title>')
    clean = "Tweets:" + '<br>'
    index = dirty.find('<title>') + 7
    endex = dirty.find('</title>')

    while occur > 0:
        index = dirty.find('<title>',index) + 7
        endex = dirty.find('</title>',index)
        temp = dirty[index:endex]


        clean = clean + temp + '<br>'
        occur = occur - 1
        

    save = open(tweets,'w')
    save.write(clean)
    save.close()


def backup():
    user = sys.argv[1]
    store = user + '_tweets.html'
    command = "curl -s --user-agent 'Mozilla' --insecure 'https://api.twitter.com/1/statuses/user_timeline.rss?screen_name="
    count = "&count=100"
    page = "&page="
    x = 1
    print "This may take a while..."
    tweet_file = open(store, 'w')
    while x < 32:
        tweets = commands.getoutput(command+user+count+page+str(x) + "'")
        tweet_file.write(tweets)
        x = x + 1
        
    tweet_file.close()

    print "Cleaning tweets"
    clean_tweets(store)

if __name__ == '__main__':
    backup()




