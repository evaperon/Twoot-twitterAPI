from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt

MONGO_HOST='mongodb://localhost'
DATABASE = '2492_2562_2592'

client = MongoClient(MONGO_HOST)
db = client[DATABASE]

collections = ['amtrak','JamesHarrison','GoldenGlobes','MondayMotivation', 'DayAfterChristmas']
sentimentLabels = { 'pos': 1, 'neutral': 0, 'neg': -1 }

def metrics(collection):
    cursor = db[collection].find()
    uniqueUserSentiment = {}
    uniqueUserRatio = {} #follower:friend ratio
    for document in cursor:
        if document['user']['id'] in uniqueUserSentiment: #We don't have to check in both dicts since both kave the unique id as key
            if (document['label'] == 'error'):
                uniqueUserSentiment[document['user']['id']] += 0
            else:
                uniqueUserSentiment[document['user']['id']] += sentimentLabels[document['label']]
        else:
            if (document['label'] == 'error'):
                uniqueUserSentiment[document['user']['id']] = 0
            else:
                uniqueUserSentiment[document['user']['id']] = sentimentLabels[document['label']]
            if (document['user']['friends_count']>0):
                uniqueUserRatio[document['user']['id']] = document['user']['followers_count'] / document['user']['friends_count']
            else:
                if (document['user']['followers_count']>0):
                    uniqueUserRatio[document['user']['id']] = 0
                else:
                    uniqueUserRatio[document['user']['id']] = 0
    return uniqueUserSentiment, uniqueUserRatio    

def userSentiment(uniqueUserSentiment,collection):
    #User Sentiment
    print("Below is the sentiment of the users around the topic : " + collection)
    for i,user in enumerate(uniqueUserSentiment):

        if ( uniqueUserSentiment[user] > 0):
            print( "user: " + repr(user) + " sentiment: positive" )
        elif ( uniqueUserSentiment[user] == 0):
            print( "user: " + repr(user) + " sentiment: neutral" )
        elif (uniqueUserSentiment[user] < 0):
            print( "user: " + repr(user) + " sentiment: negative" )

def userRatio(uniqueUserRatio,collection):
    #User follower to friend ratio
    print("Below is the follower to friend ratio of the users that posted about the topic : " + collection)
    for i,user in enumerate(uniqueUserRatio):
        print( "user: " + repr(user) + " ratio: " + repr(uniqueUserRatio[user]) )

def plotCFD(uniqueUserRatio):  
    
    plt.figure(1)
    Y = list(uniqueUserRatio.values())

    ySum = 0.0
    for i in Y:
        ySum += i
    for i, item in enumerate(Y):
        Y[i] /= ySum

    CY = np.cumsum(Y)
    
    plt.plot(Y)
    plt.plot(CY,'r--', drawstyle='steps')
    plt.title('Cumulative Frequency Distribution')

    plt.show()
    
    


for collection in collections:
    
    uniqueUserSentiment, uniqueUserRatio = metrics(collection)

    userSentiment(uniqueUserSentiment,collection)

    userRatio(uniqueUserRatio,collection)
    

    plotCFD(uniqueUserRatio)

        