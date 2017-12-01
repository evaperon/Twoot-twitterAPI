import tweepy

ckey = 'e7G34MChU43AeMNi132HY749M'
csecret = '9NE3teD2MCzW4sZlEcXaBlOsciYIoXmP3TOa2ET26dLmx11yK7'
atoken = '778561405515657216-UsYopTmE3JFIB3Fi8NZDkcZdzmvCvmG'
asecret = '1dsDu9Z2bIIFJXKfJ4pTtDjY6pTpE2OhPMoM2IJIXpAwb'

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

    
trends1 = api.trends_place(23424977)
# trends1 is a list with only one element in it, which is a 
# dict which we'll put in data.
data = trends1[0] 
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]
# put all the names together with a ' ' separating them
topFive = names[:5]
trendsName = ' '.join(topFive)
#print(trendsName)
print (topFive[0])


#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api=None):
        super().__init__()
        self.num_tweets = 0
    
    def on_status(self, status):
        if self.num_tweets<1500:
            if not status.retweeted and not status.text.startswith("RT"):
                print (status.text)
                self.num_tweets+=1
                print(self.num_tweets)
            return True
        else:
            #stop streaming
            print ("stop streaming")
            return False
          
    
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=topFive[0])