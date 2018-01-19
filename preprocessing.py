from pymongo import MongoClient
from nltk.corpus import stopwords


MONGO_HOST='mongodb://localhost/twootdb'
DATABASE = 'twootdb'

client = MongoClient(MONGO_HOST)
db = client[DATABASE]
collections = ['amtrak','JamesHarrison','GoldenGlobes','mondaymotivation', 'DayAfterChristmas']
customStopWords = {'amtrak':['amtrak', 'amtraks'],'JamesHarrison':['james','harrison','jamesharrison'],'GoldenGlobes':['golden','globes','goldenglobes'],'mondaymotivation':['monday','motivation','mondaymotivation'],'DayAfterChristmas':['day','christmas','dayafterchristmas','christmasday','afterchristmas']}


def parseTweets():
    #Load nltk stopwords 
    stopWords =  stopwords.words('english') 
    collectionsWithStopwords = []
    collectionsWithoutStopwords = []
    IDs = []
	#For every trend
    for collection in collections:
        #Load all tweets from the collection
        cursor = db[collection].find()
        tweets = []
        tweetsIds = []
        for document in cursor:
            #We don't want retweets
            if (document['retweeted']==True): 
                continue
            #Store only the text from each tweet
            tweets.append(document['text'])
            tweetsIds.append(document['_id'])

        IDs.append(tweetsIds)
        for i,tweet in enumerate(tweets):
            #Tokenization
            tweets[i] = tweet.split()        
            #Remove punctuation
            punctuation = '.?!:,$<>;`~’"-#@&*^()/\[]{}|-_+=…'
            punctuation+= "'"
            for p in punctuation:
                tweets[i][:] = [word.replace(p, "")  for word in tweets[i] ]            
            #Remove special characters, numbers and normalize the remaining words
            tweets[i][:] = [word.lower() for word in tweets[i] if word.isalpha()] 
            #Add a new field in the database with the processed tweet
            db[collection].update_one( {"_id": tweetsIds[i] },
            {"$set": {"processed_text": ' '.join(tweets[i])}})
        collectionsWithStopwords.append(tweets)
        tweetsNoStopwords = []
        for i,tweet in enumerate(tweets):
            #Remove stopwords
            tweetsNoStopwords.append( [word for word in tweets[i] if word not in stopWords and word not in customStopWords[collection]])
            #Add a new field in the database with the processed tweet without stopwords
            db[collection].update_one({"_id": tweetsIds[i] },
            {"$set": {"processed_text_no_stopwords": ' '.join(tweetsNoStopwords[i])}})
        collectionsWithoutStopwords.append(tweetsNoStopwords)
        
    #Returns the names of the processed collections, the original tweets from each collection, the tweets after we removed the stopwords and the tweets' IDs    
    return collections,collectionsWithStopwords, collectionsWithoutStopwords,IDs
        
