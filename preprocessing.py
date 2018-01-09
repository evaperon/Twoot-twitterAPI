from pymongo import MongoClient
#from nltk.corpus import stopwords
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

MONGO_HOST='mongodb://localhost/twootdb'

client = MongoClient(MONGO_HOST)
db = client.twootdb 
collections = ['amtrak','Trend2','Trend3','Trend4', 'Trend5']

#stopWords =  stopwords.words('english')

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

    #print(uniqueWords)
    sortedWords = sorted(uniqueWords.items(), key = lambda x : x[1])
    #print (sortedWords)
    sortedWords = list(reversed(sortedWords))
    top50 = sortedWords[:50]
    #print(type(top50))
	
    #for i,word in enumerate(top50):
        #print(i+1,word)
    return top50, sortedWords, wordCount


#for every trend
for collection in collections:
    #add the trend's name to the stopwords (me dedomeno oti to onoma tis sullogis einai to onoma tou trend)
    #stopWords.append( collection)     #isws prepei ki alla 
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
        #if 'amtrak' not in tweet:
            #print(tweet)
        #tokenization
        tweets[i] = tweet.split()        
        #remove punctuation
        punctuation = '.?!:’"-#'
        punctuation+= "'"
        for p in punctuation: #isws ginetai pio apodotika me REGEX?
            tweets[i][:] = [word.replace(p, "")  for word in tweets[i] ]
	
	
        #remove special characters, numbers and stopwords and normalize the remaining words
        tweets[i][:] = [word.lower() for word in tweets[i] if word.isalpha()]# and word not in stopWords] 

    top50WordsWithoutStopwordRemoval, words, wordC = countUniqueWords(tweets)
    print (wordC)
    words225 = words[:225]
    allTheWords = [i[0] for i in words225]
    allTheWordsC = [i[1] for i in words225]
    
    plt.figure(1)
    plt.subplot(211)
    plt.bar(range(len(allTheWords)),allTheWordsC, tick_label=allTheWords, align='center', color='red')
    plt.xticks(rotation='vertical')
    plt.ylabel('Word Count')
    
    #print(top50WordsWithoutStopwordRemoval)
    wordCounts = [i[1] for i in top50WordsWithoutStopwordRemoval]
    topWords = [i[0] for i in top50WordsWithoutStopwordRemoval]
    #print(wordCounts)
    #print(topWords)
    plt.subplot(212)
    plt.bar(topWords,wordCounts,align='center')
    plt.xticks(rotation='vertical')
    plt.ylabel('Word Counts')

    
    #the following commented part is for lines to show for each bar
    #but it looks bad so I scrapped it
    #for i in range(len(wordCounts)):
        #plt.hlines(wordCounts[i],0,topWords[i])
    plt.show(block=False)
