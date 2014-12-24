import twitter
import sys
import ConfigParser
#See twit_post.conf for an example configuration file
config_file = "Your configuration file (use full path if not in local directory)"

def post_status(account, status):
	#Read config file for account data
	config = ConfigParser.RawConfigParser()
	config.read(config_file)
	consumer_key = config.get('defaults', 'consumer_key')
	consumer_secret = config.get('defaults', 'consumer_secret')
	access_token_key = config.get(account, 'access_token_key')
	access_token_secret = config.get(account, 'access_token_secret')
	
	
	try:
		api = twitter.Api(consumer_key = consumer_key, consumer_secret = consumer_secret, access_token_key = access_token_key, access_token_secret = access_token_secret)	
		print status
		print 'posting to Twitter...'
		result = api.PostUpdate(status)
		print '  post successful!\n\n'
	except twitter.TwitterError:
		print ' post failed'

if __name__ == "__main__":
	post_status(sys.argv[1], sys.argv[2])
