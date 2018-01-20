import tweepy
from pymongo import MongoClient
import json

MONGO_HOST='mongodb://localhost/twootdb'
DATABASE = 'twootdb'
NUMTWEETS = 1500
NUMTRENDS = 5

#Replace with your private keys
KEY = '' 
TOKEN = ''

auth = tweepy.OAuthHandler(KEY)
auth.set_access_token(TOKEN)

api = tweepy.API(auth)

#Override tweepy.StreamListener to add logic to its methods
class MyStreamListener(tweepy.StreamListener):
    
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def __init__(self, database, collection, numTweetsToCollect, api=None):
        super().__init__()
        self.num_tweets = 0
        self.collection = collection
        self.numTweetsToCollect = numTweetsToCollect
        try:
            client = MongoClient(MONGO_HOST)            
            # Use the specified database. If it doesn't exist, it will be created.
            self.db = client[database]   
        except Exception as e:
           print(e)
    
    def on_data(self, data):
        if self.num_tweets<self.numTweetsToCollect:
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            #Filtering retweets to make sure that retweets are not taken into account
            if not (datajson['retweeted'] or datajson['text'].startswith('RT')):
                self.num_tweets+=1
                try:
                	#Insert the tweet in JSON format in a collection named after the trend 
                	#If the collection doesn't exist, it will be created
                    self.db[self.collection].insert_one(datajson)
                except Exception as e:
                   print(e)
            return True
        else:
             #Stop streaming when numTweetsToCollect tweets have been gathered
             return False

trends1 = api.trends_place(23424977)
# Trends1 is a list with only one element in it, which is a dict which we'll put in data.
data = trends1[0] 
# Grab the trends
trends = data['trends']
# Grab the name from each trend
names = [trend['name'] for trend in trends]
#Grab the first NUMTRENDS trends
topTrends = names[:NUMTRENDS]
          
#Collect NUMTWEETS tweets for every trend
for trend in topTrends:
	#Connect to the Twitter Stream
    myStreamListener = MyStreamListener(DATABASE,trend, NUMTWEETS)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    #Gather tweets only related to the specified trend and in the english language
    myStream.filter(track=[trend],languages=["en"])
