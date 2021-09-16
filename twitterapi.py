import twitter
# api = twitter.Api(consumer_key="dummy",consumer_secret="dummy",access_token_key="dummy",access_token_secret="dummy",sleep_on_rate_limit=True,application_only_auth=True)

def getfollowers(userid):
	try:
		return len(api.GetFollowers(screen_name=userid,include_user_entities=True))
	except:
		return -1

def getpost(postid):
	try:
		x=api.GetStatus(postid)
		return True
	except:
		return False