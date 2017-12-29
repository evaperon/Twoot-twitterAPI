import tweepy
#import unicodedata
from pymongo import MongoClient
import json

MONGO_HOST='mongodb://localhost/twootdb'

auth = tweepy.OAuthHandler(secret)
auth.set_access_token(secret)

api = tweepy.API(auth)

    
trends1 = api.trends_place(23424977)
# trends1 is a list with only one element in it, which is a 
# dict which we'll put in data.
data = trends1[0] 
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]
#grab the first five trends
topFive = names[:5]
# put all the names together with a ' ' separating them
trendsName = ' '.join(topFive) # why?
#print(trendsName)



#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def __init__(self, database, collection, api=None):
        super().__init__()
        self.num_tweets = 0
        self.collection = collection
        try:
            client = MongoClient(MONGO_HOST)            
            # Use twootdb database. If it doesn't exist, it will be created.
            self.db = client[database]   
        except Exception as e:
           print(e)
    
    def on_data(self, data):
        if self.num_tweets<1500:
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            #filerin retweets
            if not (datajson['retweeted'] or datajson['text'].startswith('RT')):
                #tweet=''.join(c for c in unicodedata.normalize('NFC', data.text) if c <= '\uFFFF')
                #print (tweet)
                self.num_tweets+=1
                try:
                    self.db[self.collection].insert_one(datajson)
                except Exception as e:
                   print(e)
            return True
        else:
             #stop streaming
             return False
          
for trend in topFive:
    myStreamListener = MyStreamListener('twootdb',trend)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=[trend],languages=["en"])
