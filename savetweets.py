from TweetStore import TweetStore
from TwitterAPI.TwitterAPI import TwitterAPI


COUCH_DATABASE = 'test_db'
TWITTER_ENDPOINT = 'statuses/filter'
TWITTER_PARAMS = {'track':'taarangana'}

API_KEY = 'xTEdIvzBj3LTrwLRUuf84SyxM'
API_SECRET = 'IX9NUd48EBccw0d3D1A0QiUaS79DlXhkVfZyOy5ZdBfPtOV3dW'
ACCESS_TOKEN = '566861858-HhaAzNvqvNont9Ft9nIBgHkjBl06kG3aupwQBBHC'
ACCESS_TOKEN_SECRET = 'YuAjsEkTGGTMdZoGyJVF7WmdxUHK4eUf4NNhKOFIMK3cr'

storage = TweetStore(COUCH_DATABASE)

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


for item in api.request(TWITTER_ENDPOINT, TWITTER_PARAMS):
	if 'text' in item:
		print('%s -- %s\n' % (item['user']['screen_name'], item['text']))
		storage.save_tweet(item)
	elif 'message' in item:
		print('ERROR %s: %s\n' % (item['code'], item['message']))
