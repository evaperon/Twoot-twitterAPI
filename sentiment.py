from pymongo import MongoClient
import requests
from preprocessing import parseTweets

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 

collections, collectionsWithStopwords, collectionsWithoutStopwords, tweetsIds = parseTweets()

tweetsWithLabels = {}
count = 0
for i,collection in enumerate(collectionsWithoutStopwords):
    for j,tweet in enumerate(collection):
        try:
            strTweet = ' '.join(tweet)
            print(strTweet)        
            r = requests.post("http://text-processing.com/api/sentiment/", data={'text':strTweet })
            print(r.status_code, r.reason)
            print(r.json())
            count += 1
            up=db[collections[i]].update_one(
            {"_id": tweetsIds[i][j] },
            {"$set": {"label": r.json()['label'], "positive_probability": r.json()['probability']['pos'] , "negative_probability": r.json()['probability']['neg'] ,"neutral_probability": r.json()['probability']['neutral']}})
            print(up.matched_count)
            print(count)
        except: #(r.status_code == 400):
            #Empty tweet or other problem
            count += 1
            up=db[collections[i]].update_one(
            {"_id": tweetsIds[i][j] },
            {"$set": {"label": 'error', "positive_probability": 0 , "negative_probability": 0 ,"neutral_probability": 0}})
            print(up.matched_count)
            print(count)
                 
