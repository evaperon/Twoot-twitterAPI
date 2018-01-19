from pymongo import MongoClient
import requests
from preprocessing import parseTweets

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 

collections, collectionsWithStopwords, collectionsWithoutStopwords, tweetsIds = parseTweets()

def addSentiment():
    count = 0
    for i,collection in enumerate(collectionsWithoutStopwords):
        for j,tweet in enumerate(collection):
            try:
                strTweet = ' '.join(tweet) #Transform the list to a string        
                r = requests.post("http://text-processing.com/api/sentiment/", data={'text':strTweet })
                #print(r.status_code, r.reason)
                #print(r.json())
                count += 1
                db[collections[i]].update_one(
                {"_id": tweetsIds[i][j] },
                {"$set": {"label": r.json()['label'], "positive_probability": r.json()['probability']['pos'] , "negative_probability": r.json()['probability']['neg'] ,"neutral_probability": r.json()['probability']['neutral']}})
            except: #(r.status_code == 400 or 503):
                #Empty tweet or other problem
                db[collections[i]].update_one(
                {"_id": tweetsIds[i][j] },
                {"$set": {"label": 'error', "positive_probability"  : 0 , "negative_probability": 0 ,"neutral_probability": 0}})
            
def pies():
    for collection in collections:
        frequencies = {'pos': 0, 'neutral': 0, 'neg': 0, 'error':0 }
        #Load all tweets from the collection
        cursor = db[collection].find()
        for document in cursor:
            frequencies[document['label']]+=1
        print(frequencies)
        #Plot pie
     
#Uncomment in order to run the above
'''  
addSentiment()          
pies()
'''