from pymongo import MongoClient
from nltk.corpus import stopwords


MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb
collections = ['amtrak','JamesHarrison','GoldenGlobes','mondaymotivation', 'DayAfterChristmas']
customStopWords = {'amtrak':['amtrak', 'amtraks'],'JamesHarrison':['james','harrison','jamesharrison'],'GoldenGlobes':['golden','globes','goldenglobes'],'mondaymotivation':['monday','motivation','mondaymotivation'],'DayAfterChristmas':['day','christmas','dayafterchristmas','christmasday','afterchristmas']}


def parseTweets():
    #for every trend
    stopWords =  stopwords.words('english')
    collectionsWithStopwords = []
    collectionsWithoutStopwords = []
    IDs = []
    for collection in collections:

        #load all tweets from the collection
        cursor = db[collection].find()
        tweets = []
        tweetsIds = []
        for document in cursor:
            #we don't want retweets
            if (document['retweeted']==True):  
                continue
            #store only the text from each tweet
            tweets.append(document['text'])
            tweetsIds.append(document['_id'])

        IDs.append(tweetsIds)
        for i,tweet in enumerate(tweets):
            #tokenization
            tweets[i] = tweet.split()        
            #remove punctuation
            punctuation = '.?!:,$<>;`~’"-#@&*^()/\[]{}|-_+=…'
            punctuation+= "'"
            for p in punctuation:
                tweets[i][:] = [word.replace(p, "")  for word in tweets[i] ]
    
    	
            
            #remove special characters, numbers and stopwords and normalize the remaining words
            tweets[i][:] = [word.lower() for word in tweets[i] if word.isalpha()] 
 
        collectionsWithStopwords.append(tweets)
        tweetsNoStopwords = []
        for i,tweet in enumerate(tweets):
            tweetsNoStopwords.append( [word for word in tweets[i] if word not in stopWords and word not in customStopWords[collection]])
        collectionsWithoutStopwords.append(tweetsNoStopwords)
        
    #returns the original collections, the collections after we removed the stopwords and the tweets' IDs    
    return collections,collectionsWithStopwords, collectionsWithoutStopwords,IDs
        
