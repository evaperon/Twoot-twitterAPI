from pymongo import MongoClient
from nltk.corpus import stopwords
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import string

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 
collections = ['amtrak']#,'Trend2','Trend3','Trend4', 'Trend5']

stopWords =  stopwords.words('english')

#this function returns the 50 most used words and the whole list of unique word
#and the times they appear in the collection and the collection's word count
def countUniqueWords(tweets):
    #print(len(tweets))
    uniqueWords = {}
    wordCount = 0
    for tweet in tweets:            
        for word in tweet:
            #print (word)
            wordCount += 1
            if word in uniqueWords:
                 uniqueWords[word] += 1
            else:
                 uniqueWords[word] = 1

    #print(uniqueWords) #dangerous
    sortedWords = sorted(uniqueWords.items(), key = lambda x : x[1])
    #print (sortedWords) #dangerous
    sortedWords = list(reversed(sortedWords))
    top50 = sortedWords[:50]
    #print(type(top50))
	
    #for i,word in enumerate(top50):
        #print(i+1,word)
    return top50, sortedWords, wordCount

def doThePlots(top50Words, words, wordC):
    #print (wordC)
    words100 = words[:100]
    allTheWords = [i[0] for i in words100]
    allTheWordsC = [i[1] for i in words100]
    
    #print(top50WordsWithoutStopwordRemoval)
    wordCounts = [i[1] for i in top50Words]
    topWords = [i[0] for i in top50Words]
    #print(wordCounts)
    #print(topWords)
    
    plt.figure(1)
    #plotting the word count of the top 50 words
    #plt.subplot(212)
    plt.bar(topWords,wordCounts,align='center')
    plt.xticks(rotation='vertical')
    plt.ylabel('Word Counts')
    
    
    plt.figure(2)
    #plotting the Zipf diagram
    #plt.subplot(211)
    plt.plot(range(len(allTheWords)), allTheWordsC, color='red')
    #plt.bar(range(len(allTheWords)), allTheWordsC, tick_label=' ', align='center', color='red')
    #plt.xticks(range(len(allTheWords)), allTheWords, rotation='vertical')
    plt.ylabel('Zipf')

    #plotting the zipf diagram curve in loglog scale
    plt.figure(3)
    plt.loglog(range(len(allTheWords)), allTheWordsC)
    #plt.xticks(range(len(allTheWords)), allTheWords, rotation='vertical')
    plt.ylabel('Word Count')
    
    #the following commented part is for lines to show for each bar
    #but it looks bad so I scrapped it
    #for i in range(len(wordCounts)):
    #plt.hlines(wordCounts[i],0,topWords[i])
    
    plt.show()

def parseTweets():
    #for every trend
    collectionsWithStopwords = []
    collectionsWithoutStopwords = []
    IDs = []
    
    for collection in collections:
        #add the trend's name to the stopwords (me dedomeno oti to onoma tis sullogis einai to onoma tou trend)
        #stopWords.append( collection)     #isws prepei ki alla 
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
            #if 'amtrak' not in tweet:
                #print(tweet)
            #tweets[i].translate(string.maketrans("",""), string.punctuation)
            #tokenization
            tweets[i] = tweet.split()        
            #remove punctuation
            punctuation = '.?!:,$<>;`~’"-#@&*^()/\[]{}|-_+=…'
            punctuation+= "'"
            for p in punctuation: #isws ginetai pio apodotika me REGEX?
                tweets[i][:] = [word.replace(p, "")  for word in tweets[i] ]
    
    	
            
            #remove special characters, numbers and stopwords and normalize the remaining words
            tweets[i][:] = [word.lower() for word in tweets[i] if word.isalpha()  ] 
            #print(tweets[i])  
 
        collectionsWithStopwords.append(tweets)
        #print(tweets[0])
        tweetsNoStopwords = []
        for i,tweet in enumerate(tweets):
            tweetsNoStopwords.append( [word for word in tweets[i] if word not in stopWords and word != collection])
        #print(tweetsNoStopwords[0])
        collectionsWithoutStopwords.append(tweetsNoStopwords)
        
        
    return collectionsWithStopwords, collectionsWithoutStopwords, IDs


def main():
    
    collectionsWithStopwords,collectionsWithoutStopwords,dummy = parseTweets()  
    for collection in collectionsWithStopwords:    
        top50WordsWithoutStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(top50WordsWithoutStopwordRemoval, words, wordC)
    
    for collection in collectionsWithoutStopwords:    
        top50WordsWithStopwordRemoval, words, wordC = countUniqueWords(collection)
        doThePlots(top50WordsWithStopwordRemoval, words, wordC)

if __name__ == "__main__":
    main()
