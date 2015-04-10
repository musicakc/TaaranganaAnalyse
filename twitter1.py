import couchdb
import couchdb.design

class TweetStore(object):
    def __init__(self,dbname,url='http://127.0.01:5984/'):
        try:
            self.server=couchdb.Server(url=url)
            self.db=self.server.create(dbname)
            self._create_views()
        except couchdb.http.PreconditionFailed:
            self.db=self.server[dbname]

    def _create_views(self):
        count_map='function(doc) {emit(doc.id, 1);}'
        count_reduce='function(keys,values) {return sum(values);}'
        view=countdb.design.ViewDefinition('twitter','count_tweets',count_map,reduce_fun=count_reduce)
        view.sync(self.db)
        get_tweets='function(doc) {emit((""0000000000000000000"+doc.id).slice(-19),doc);}'
        view=couchdb.design.ViewDefinition('twitter','get_tweets',get_tweets)
        view.sync(self.db)

    def save_tweet(self,tw):
        tw['_id']=tw['id_str']
        self.db.save(tw)

    def count_tweets(self):
        for doc in self.db.view('twitter/count_tweets'):
            return doc.value

    def get_tweets(self):
        return self.db.view('twitter/get_tweets')
        
from TweetStore import TweetStore
from TwitterAPI.TwitterAPI import TwitterAPI

api_key=''
api_secret=''
access_token=''
access_secret=''

storage=TweetStore('test_db')
api=TwitterAPI(api_key,api_secret,access_token,access_secret)

for item in api.request('search/tweets',{'q':'taarangana'}):
    if 'text' in item:
        print('%s -- %s\n' % (item['user']['screen_name'],item['text']))
        storage.save_tweet(item)
    elif 'message' in item:
        print('ERROR %s: %s\n' % (item['code'],item['message']))
