#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
import math

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 

collections = [ 'amtrak'] #, 'DayaAfterChristmas', 'GoldenGlobes', 'JamesHarrison', 'mondaymotivation']

sentimentLabels = { 'pos': 1, 'neutral': 0, 'neg': -1 }

def metrics(collection):
    cursor = db[collection].find()
    uniqueUserSentiment = {}
    uniqueUserRatio = {} #follower:friend ratio
    for document in cursor:
        if document['user']['id'] in uniqueUserSentiment: #we don't have to check in both dicts since both kave the unique id as key
            #print(document['label'])
            if (document['label'] == 'error'):
                uniqueUserSentiment[document['user']['id']] += 0
            else:
                uniqueUserSentiment[document['user']['id']] += sentimentLabels[document['label']]
        else:
            #print(document['label'])
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
        #print(type(uniqueUserSentiment))
        #print(type(user))

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
        #print(type(uniqueUserRatio))
        #print(type(user))
        
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


    plt.subplot(211)
    #plt.plot(Y, drawstyle='steps')
    plt.plot(CY,'r--', drawstyle='steps')
    
    plt.subplot(212)
    #plt.plot(Y)
    plt.plot(CY,'r--')
    
    plt.show()
    
    

def main():
    for collection in collections:
        
        uniqueUserSentiment, uniqueUserRatio = metrics(collection)

        '''userSentiment(uniqueUserSentiment,collection)

        userRatio(uniqueUserRatio,collection)'''
        

        plotCFD(uniqueUserRatio)

        

if __name__ == "__main__":
    main()
