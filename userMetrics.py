#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 
collections = ['amtrak']#,'Trend2','Trend3','Trend4', 'Trend5']
sentimentLabels = { 'pos': 1, 'neutral': 0, 'neg': -1 }

def metrics(collection):
    cursor = db[collection].find()
    uniqueUserSentiment = {}
    uniqueUserRatio = {} #follower:friend ratio
    for document in cursor:
        if document['user']['id'] in uniqueUserSentiment: #we don't have to check in both dicts since both kave the unique id as key
            print(document['label'])
            uniqueUserSentiment[document['user']['id']] += sentimentLabels[document['label']]
        else:
            uniqueUserSentiment[document['user']['id']] = sentimentLabels[document['label']]
            if (document['user']['friends_count']>0):
                uniqueUserRatio[document['user']['id']] = document['user']['followers_count'] / document['user']['friends_count']
            else:
                #WHAT?
                x=5
    return uniqueUserSentiment, uniqueUserRatio    

def userSentiment(uniqueUserSentiment,collection):
    #User Sentiment
    print("Below is the sentiment of the users around the topic : " + collection)
    for i,user in enumerate(uniqueUserSentiment):
        print([user], user[i])

def userRatio(uniqueUserRatio,collection):
    #User follower to friend ratio
    print("Below is the follower to friend ratio of the users that posted about the topic : " + collection)
    for i,user in enumerate(uniqueUserRatio):
        print([user], user[i])

def plotCFD(uniqueUserRatio):
    #first idea, untested
    '''figure(1)
    n, bins, patches = plt.hist(uniqueUserRatio, len(uniqueUserRatio), histtype='step', cumulative=True)
    plt.grid(True)
    plt.title('Cumulative Frequency Distribution')

    plt.show()'''

    #second idea, contains two methods, also untested
    '''N = len(uniqueUserRatio)
    Z = uniqueUserRatio
    # method 1
    H,X1 = np.histogram( Z, bins = 10, normed = True )
    dx = X1[1] - X1[0]
    F1 = np.cumsum(H)*dx
    #method 2
    X2 = np.sort(Z)
    F2 = np.array(range(N))/float(N)

    plt.plot(X1[1:], F1)
    plt.plot(X2, F2)
    plt.show()'''
    

def main():
    for collection in collections:
        
        uniqueUserSentiment, uniqueUserRatio = metrics(collection)

        '''userSentiment(uniqueUserSentiment,collection)

        userRatio(uniqueUserRatio,collection)'''
        

        #plotCFD(uniqueUserRatio)

        

if __name__ == "__main__":
    main()
