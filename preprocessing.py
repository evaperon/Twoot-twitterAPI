from pymongo import MongoClient
from nltk.corpus import stopwords

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 
collections = ['Trend1','Trend2','Trend3','Trend4', 'Trend5']

stopWords =  stopwords.words('english')

#for every trend
for collection in collections:
    #add the trend's name to the stopwords (me dedomeno oti to onoma tis sullogis einai to onoma tou trend)
    stopWords.append( collection)     #isws prepei ki alla 
    #load all tweets from the collection
    cursor = db[collection].find()
    tweets = []
    for document in cursor:
        #we don't want retweets
        if (document['retweeted']==True):  
            continue
        #store only the text from each tweet
        tweets.append(document['text'])
          
    for i,tweet in enumerate(tweets):        
        #tokenization
        tweets[i] = tweet.split()        
        #remove punctuation
        punctuation = '.?!:’"-'
        punctuation+= "'"
        for p in punctuation: #isws ginetai pio apodotika me REGEX?
            tweets[i][:] = [word.replace(p, "")  for word in tweets[i] ]
        #oremove special characters, numbers and stopwords and normalize the remaining words
        tweets[i][:] = [word.lower() for word in tweets[i] if word.isalpha() and word not in stopWords] 
        
        
         

        
    
