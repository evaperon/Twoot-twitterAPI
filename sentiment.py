from pymongo import MongoClient
import requests
from preprocessing import parseTweets
import matplotlib.pyplot as plt

MONGO_HOST='mongodb://localhost'
DATABASE = '2492_2562_2592'

client = MongoClient(MONGO_HOST)
db = client[DATABASE]

collections, collectionsWithStopwords, collectionsWithoutStopwords, tweetsIds = parseTweets()

def addSentiment():
    count = 0
    for i,collection in enumerate(collectionsWithoutStopwords):
        for j,tweet in enumerate(collection):
            try:
                strTweet = ' '.join(tweet) #Transform the list to a string        
                r = requests.post("http://text-processing.com/api/sentiment/", data={'text':strTweet })
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
        labels = list(frequencies.keys())[:3]
        sizes = list(frequencies.values())[:3]
        plotColors= '#38C477', 'khaki', '#F2543D'
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plotColors)
        ax1.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Sentiment ratio for  <' + collection+ '>')
plt.show()
     
#Uncomment in order to run the above
'''  
addSentiment()       
pies()
'''
