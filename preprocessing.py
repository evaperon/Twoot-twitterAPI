from pymongo import MongoClient
from nltk.corpus import stopwords
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import string


MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb
collections = ['amtrak','JamesHarrison','GoldenGlobes','mondaymotivation', 'DayAfterChristmas']
customStopWords = [['amtrak', 'amtraks'],['james','harrison','jamesharrison'],['golden','globes','goldenglobes'],['monday','motivation','mondaymotivation'],['day','christmas','dayafterchristmas','christmasday','afterchristmas']]

#this function returns the 50 most used words and the whole list of unique word
#and the times they appear in the collection and the collection's word count
def countUniqueWords(tweets):
    uniqueWords = {}
    wordCount = 0
    for tweet in tweets:            
        for word in tweet:
            wordCount += 1
            if word in uniqueWords:
                 uniqueWords[word] += 1
            else:
                 uniqueWords[word] = 1
    sortedWords = sorted(uniqueWords.items(), key = lambda x : x[1])
    sortedWords = list(reversed(sortedWords))
    top50 = sortedWords[:50]
    return top50, sortedWords, wordCount

def doThePlots(top50Words, words, wordC, count):
    words100 = words[:100]
    allTheWords = [i[0] for i in words100]
    allTheWordsC = [i[1] for i in words100]
    
    wordCounts = [i[1] for i in top50Words]
    topWords = [i[0] for i in top50Words]
    
    plt.figure(1)
    #plotting the word count of the top 50 words
    plt.bar(topWords,wordCounts,align='center')
    plt.xticks(rotation='vertical')
    plt.title('Word Counts for <' + collections[count] + '>')
    
    '''
    plt.figure(2)
    #plotting the Zipf diagram
    plt.plot(range(len(allTheWords)), allTheWordsC, color='red')
    plt.title('Zipf for <' + collections[count] + '>')

    #plotting the zipf diagram curve in loglog scale
    plt.figure(3)
    plt.loglog(range(len(allTheWords)), allTheWordsC)
    plt.title('Zipf logarithmic scale for <' + collections[count] + '>')'''
    
    plt.show()

def parseTweets():
    #for every trend
    stopWords =  stopwords.words('english')
    collectionsWithStopwords = []
    collectionsWithoutStopwords = []
    IDs = []
    j = 0
    for collection in collections:

        #load all tweets from the collection
        stopWords.extend(customStopWords[j])
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
            tweetsNoStopwords.append( [word for word in tweets[i] if word not in stopWords])
        collectionsWithoutStopwords.append(tweetsNoStopwords)
        for i, item in enumerate(customStopWords[j]):
            stopWords.remove(customStopWords[j][i])
        #stopWords = stopWords[:len(stopWords)-len(customStopWords[j])]
        #^this might be faster than remove according to this https://stackoverflow.com/questions/5745881/fast-way-to-remove-a-few-items-from-a-list-queue
        j += 1
    #returns the original collections, the collections after we removed the stopwords and the tweets' IDs    
    return collectionsWithStopwords, collectionsWithoutStopwords,IDs
        
def main():
    
    collectionsWithStopwords,collectionsWithoutStopwords, dump = parseTweets()
    i = 0
    for collection in collectionsWithStopwords:    
        top50WordsWithoutStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(top50WordsWithoutStopwordRemoval, words, wordC, i)
        i += 1
    i = 0
    for collection in collectionsWithoutStopwords:    
        top50WordsWithStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(top50WordsWithStopwordRemoval, words, wordC, i)
        i += 1

if __name__ == "__main__":
    main()
